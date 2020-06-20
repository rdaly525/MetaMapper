import pulp

#Solve Binate Covering problem

Var = lambda name: pulp.LpVariable(name, cat='Integer')
x = Var('x')
y = Var('y')

p = pulp.LpProblem("BS", pulp.LpMinimize)

#Objective
p += 4*x+3*y, "Z"

#Constraints
p += (2*y <= 25-x)
p += (4*y >=2*x-8)
p += (y <=2*x-5)
p += (y>=0)
p += (x>=0)
print(p)
p.solve()
print(p.status)
print(p.variables())
print(x.name, x.varValue)

#Lets say I have graph
#Expr = Add(Mul(a,b),c)
#
#T1 = Mul(i0,i1)
#T2 = Add(i0,i1)
#T0 = Add(Mul(i0,i1),i2)
