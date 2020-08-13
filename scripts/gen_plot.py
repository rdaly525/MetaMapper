import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np

path = "results/riscv_ext"

tdata = {}
fdata = {}
num_files = 5
for i in range(num_files):
    file = f"{path}/z3_{i}.txt"
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
    assert len(set(f)) == 1
    print(n1, f, t)

x_pos = list(range(len(fdata)))
mean_time = [np.mean(val) for val in tdata.values()]
min_time = [np.mean(val)-np.min(val) for val in tdata.values()]
max_time = [np.max(val)-np.min(val) for val in tdata.values()]
col = ["green" if f[0] else "red" for f in fdata.values()]
names = list(tdata.keys())
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
plt.show()
