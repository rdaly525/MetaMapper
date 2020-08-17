import delegator

def gen():
    cpath = "results/hd"
    for i in range(1,26):
        p = f"p{i}"
        cfile = f"results/hd/{p}.c"
        sfile = f"results/hd_results/{p}.s"
        cmd = f"riscv64-unknown-elf-gcc -march=rv32i -mabi=ilp32 -Og -S {cfile} -o {sfile}"
        res = delegator.run(cmd)
        assert not res.return_code, res.out + res.err

#gen()

def cnt(i):
    p = f"p{i}"
    sfile = f"results/hd_results/{p}.s"
    program = []
    with open(sfile, "r") as f:
        start = False
        for line in f.readlines():
            if line[:len(p)] == p:
                start = True
                continue
            if start:
                if 'size' in line:
                    break
                if line[0] == ".":
                    continue
                else:
                    program.append(line[:-1])
    res_file = "results/real_asm_cnt.txt"
    with open(res_file, "a") as f:
        print(f"{i}:{len(program)}", file=f)

for i in range(1,26):
    cnt(i)
