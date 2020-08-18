import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np


#This script generates a graph of the 3 extensions and the times of each op

def gen():
    e=True
    fig = plt.figure()
    data = {}
    for solver in ("cvc4", "btor"):
        for c in (True, False):
            r = "riscv"
            #for ri, r in enumerate(("riscv", "riscv_ext", "riscv_m")):
            path = f"results/{r}"
            tdata = {}
            fdata = {}
            num_files = 3
            name  = f"{solver}_c{c}_e{e}"
            for i in range(num_files):
                for file in (
                    f"{path}/{name}_{i}.txt",
                ):
                    with open(file, "r") as f:
                        lines = f.readlines()
                        for line in lines:
                            n,t,found = line.split(": ")
                            #n = n[4:]
                            found = found[0]
                            tdata.setdefault(n, np.zeros(num_files))
                            tdata[n][i] = t
                            fdata.setdefault(n, [])
                            fdata[n].append(found=="f")


            for (n1, f), (n2, t) in zip(fdata.items(), tdata.items()):
                assert n1 == n2
                #print(n1, f, t)
            mean_time = [np.mean(val) for val in tdata.values()]
            data[(c, solver)] = mean_time
            num_ops = len(mean_time)

    #For stacked barchart
    bars = [[] for _ in range(num_ops)]
    for i in range(num_ops):
        for k, v in data.items():

            bars[i].append(v[i])

    tot = []
    names = []
    for k, v in data.items():
        print(k)
        if k[0]:
            name = "constrained"
        else:
            name = "unconstrained"
        names.append(f"{k[1]}, {name}")
        tot.append(sum(v)/60)

    x_pos = list(range(4))
    #for i in range(num_ops):
    #    bottom_bars = [0 for _ in range(4)]
    #    for k in range(i,num_ops):
    #        for j in range(4):
    #            bottom_bars[j] += bars[k][j]
    #    cur_bar = bars[i]
    #    print(bottom_bars)
    #    print(cur_bar)
    #    if i==0:
    #        plt.bar(x_pos, cur_bar, color="blue", edgecolor="white", width=1)
    #    else:
    #        plt.bar(x_pos, cur_bar, bottom=bottom_bars, color="blue", edgecolor="white", width=1)

    plt.bar(x_pos, tot, color="blue", edgecolor="white", width=0.5)



    plt.ylabel("Time (min)")
    plt.xticks(x_pos, names, rotation=75)
    plt.title("SMT performance comparison")
    plt.savefig(f"results/figs/riscv-smt-perf.png", bbox_inches='tight')
    plt.show()

gen()
