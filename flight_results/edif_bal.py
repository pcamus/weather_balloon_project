# File: edif_bal.py
# Weather balloon integration of differential equation
# Uses separation of variable method
# The equation is: dv/dt + A v**2 - B = 0
# That is in separation of varaible form: dv/(B-Av**2) = dt
# To get the solution we integrate both member (the first with sympy),
# identify the integration constant and solve the expression to get v (by hand)
# philippe.camus@hepl.be
# 5/10/2022

import sympy as sp  # sympy.org

sp.init_printing(use_unicode=False)

v = sp.Symbol('v', real=True, positive=True)
A = sp.Symbol('A', real=True, positive=True)
B = sp.Symbol('B', real=True, positive=True)
expr=1/(B-A*v**2)
sp.pprint(expr)
print("\n") # skip 2 lines

primit=sp.Integral(expr,v) # Deffered calculation
sp.pprint(primit)
print("\n") # skip 2 lines

result=primit.doit()
sp.pprint(result)
