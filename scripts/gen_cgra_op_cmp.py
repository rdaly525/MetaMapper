import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np


#This script generates a graph of the 3 extensions and the times of each op
tdata = dict(B={},A={},L={})
fdata = dict(B={},A={},L={})
def parse():
    file = "results/cgra_op_time.txt"
    with open(file, "r") as f:
        lines = f.read().splitlines()
        for line in lines[1:]:
            op, peB, peA, peL = line.split(":")
            if peA[-2:] == ",0":
                fdata["A"][op] = False
                peA = peA[:-2]
            else:
                fdata["A"][op] = True
            if peL[-2:] == ",0":
                fdata["L"][op] = False
                peL = peL[:-2]
            else:
                fdata["L"][op] = True
            fdata["B"][op] = True
            tdata["B"][op] = peB
            tdata["A"][op] = peA
            tdata["L"][op] = peL

def gen():
    fig, axs = plt.subplots(nrows=3, sharex=True)
    ops = list(tdata["A"].keys())
    for pei, pe in enumerate(("L", "A", "B")):
        x_pos = list(range(len(ops)))
        mean_time = [float(tdata[pe][op]) for op in ops]
        tot_s = sum(mean_time)
        print(f"{pe}, {tot_s//60}min {tot_s%60}sec")
        #min_time = [np.mean(val)-np.min(val) for val in tdata.values()]
        #max_time = [np.max(val)-np.min(val) for val in tdata.values()]
        col = ["green" if fdata[pe][op] else "red" for op in ops]
        names = ops
        axs[pei].bar(
            x_pos,
            mean_time,
            color = col,
            #yerr= [min_time, max_time],
            capsize=5.0,
        )
        if pei==0:
            green_p = mp.Patch(color="green", label="1 Instruction")
            red_p = mp.Patch(color="red", label="Impossible")
            axs[pei].legend(handles=[green_p, red_p], loc="upper right")
        axs[pei].set_ylabel("Time (s)")
        axs[pei].set_title(f"PE {pe}")
    plt.xticks(x_pos, names, rotation=75)
    plt.savefig(f"results/figs/cgra_op_cmp.png")
    plt.show()

parse()
gen()
