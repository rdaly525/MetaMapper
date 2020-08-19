import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np


def gen(r, solver, c, e):
    path = f"results/{r}"
    tdata = {}
    fdata = {}
    num_files = 3
    name  = f"{solver}_c{c}_e{e}"
    for i in range(num_files):
        file = f"{path}/{name}_{i}.txt"
        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines:
                n,t,found = line.split(": ")
                n = n[4:]
                found = found[0]
                tdata.setdefault(n, np.zeros(num_files))
                tdata[n][i] = t
                fdata.setdefault(n, [])
                fdata[n].append(found=="f")


    for (n1, f), (n2, t) in zip(fdata.items(), tdata.items()):
        assert n1 == n2
        #print(n1, f, t)

    x_pos = list(range(len(fdata)))
    mean_time = [np.mean(val) for val in tdata.values()]
    tot_s = sum(mean_time)
    print(f"{r}:{name}, {tot_s//60}min {tot_s%60}sec")
    min_time = [np.mean(val)-np.min(val) for val in tdata.values()]
    max_time = [np.max(val)-np.min(val) for val in tdata.values()]
    col = ["blue" if len(set(f)) != 1 else ("green" if f[0] else "red") for f in fdata.values()]
    names = list(tdata.keys())
    plt.figure()
    plt.bar(
        x_pos,
        mean_time,
        color = col,
        yerr= [min_time, max_time],
        capsize=5.0,
    )
    plt.ylabel("Time (s)")
    plt.xlabel("Op")
    plt.xticks(x_pos, names, rotation=60)

    green_p = mp.Patch(color="green", label="Rewrite Found")
    red_p = mp.Patch(color="red", label="Rewrite Not Found")
    plt.legend(handles=[green_p, red_p])
    if r == "riscv_ext":
        r = "riscv-ext"
    plt.savefig(f"results/figs/{r}-{solver}-c{c}-e{e}.png")


gen("riscv", "cvc4", c=True, e=True)
gen("riscv", "cvc4", c=False, e=True)
gen("riscv", "btor", c=True, e=True)
gen("riscv", "btor", c=False, e=True)
gen("riscv_ext", "cvc4", c=True, e=True)
gen("riscv_ext", "cvc4", c=False, e=True)
gen("riscv_ext", "btor", c=True, e=True)
gen("riscv_ext", "btor", c=False, e=True)

