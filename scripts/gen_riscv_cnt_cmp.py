import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np


#This script generates a graph for comparing instruction count

cmp_dict = {}
def parse_real(opt):
    real_file = f"results/real{opt}_asm_cnt.txt"
    cmp_dict[opt] = {}
    with open(real_file, "r") as f:
        for line in f.readlines():
            i, cnt = line.split(":")
            i = int(i)
            cnt = int(cnt[:-1])
            cmp_dict[opt][i] = cnt

flow_m = {}
def parse_flow():
    real_file = f"results/flow_asm_cnt.txt"
    cmp_dict["flow"] = {}
    with open(real_file, "r") as f:
        for line in f.readlines():
            i, m, cnt, p, t = line.split(":")
            i = int(i)
            cnt = int(cnt)
            m = m[1]
            cmp_dict["flow"][i] = cnt
            flow_m[i] = m

parse_real(0)
parse_real(1)
parse_flow()


for i in range(1,26):
    print(f"P{i} & {cmp_dict['flow'][i]} & {cmp_dict[0][i]} & {cmp_dict[1][i]}")


#Creating a bar chart with multiple groups
bar_width = 0.25
fig = plt.figure()
bar0 = [cmp_dict[0][i] for i in range(1,26)]
bar1 = [cmp_dict[1][i] for i in range(1,26)]
barflow = [cmp_dict["flow"][i] for i in range(1,26)]

r1 = np.arange(25)
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

plt.bar(r1, bar0, color="red", width=bar_width, edgecolor="white", label="gcc -O0")
plt.bar(r2, bar1, color="blue", width=bar_width, edgecolor="white", label="gcc -O1")
plt.bar(r3, barflow, color="green", width=bar_width, edgecolor="white", label="Flow")

plt.xlabel('Hackers Delight Program')
plt.ylabel('Number of RISV Instructions')
plt.xticks([r+bar_width for r in range(25)], [str(i) for i in range(1,26)])

plt.legend()
plt.show()

