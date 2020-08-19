import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np


#This script generates a graph of the 3 extensions and the times of each op

def gen():
    c=True
    e=True
    solver="btor"
    fig, axs = plt.subplots(nrows=1, sharex=True)
    #for ri, r in enumerate(("riscv", "riscv_ext", "riscv_m")):
    for ri, r in enumerate(("riscv",)):
        path = f"results/{r}"
        tdata = {}
        fdata = {}
        num_files = 3
        name  = f"{solver}_c{c}_e{e}"
        for i in range(num_files):
            for file in (
                f"{path}/{name}_r2_{i}_.txt",
            ):
                with open(file, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        n,t,found = line.split(": ")
                        if n == "const20":
                            n = "const[20]"
                        #n = n[4:]
                        found = found[0]
                        tdata.setdefault(n, np.zeros(num_files))
                        tdata[n][i] = float(t)/60 #in minutes
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
        ax = axs
        #axs[ri].bar(
        ax.bar(
            x_pos,
            mean_time,
            color = col,
            yerr= [min_time, max_time],
            capsize=3.0,
        )
        #if ri==0:
        #    green_p = mp.Patch(color="green", label="1 Instruction")
        #    red_p = mp.Patch(color="red", label="Impossible in 1 or 2")
        #    axs[ri].legend(handles=[green_p, red_p], loc="upper right")
        ax.set_ylabel("Time (min)")
        ax.set_title("Synthesis of 2 RiscV Instructions")
    plt.xticks(x_pos, names, rotation=75)
    plt.savefig(f"results/figs/riscv2-op-cmp.png", bbox_inches='tight')
    plt.show()

gen()
