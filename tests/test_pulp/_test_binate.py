import pulp

#Solve Binate Covering problem
#Lets say I have graph
#Expr = Add(Mul(a,b),c)  Add is 0, Mul is 1
#
#T0 = Mul(i0,i1), Cost(1)
#T1 = Add(i0,i1), Cost(1)
#T2 = Add(Mul(i0,i1),i2), Cost(1)

Var = lambda name: pulp.LpVariable(name, cat='Binary')
M01 = Var("M01")
M10 = Var("M10")
M20 = Var("M20")

p = pulp.LpProblem("BS", pulp.LpMinimize)

#Objective
p += M01+M10+M20

#Constraints
p += (M01 + M20==1) #v0
p += (M10 + M20==1) #v1
print(p)
p.solve()
print(p.status)
for v in p.variables():
    print(f"{v.name} = {v.varValue}")
