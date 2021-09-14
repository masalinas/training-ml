# Import PuLP modeler functions
# sudo apt install libglpk-dev
# pip install glpk
# sudo apt-get install glpk-utils
# https://www.gurobi.com/
# https://www.cplex.com/

from pulp import *
import pulp as pl

# Create the 'prob' variable to contain the problem data
prob = LpProblem("The Whiskas Problem", LpMinimize)

# The 2 variables Beef and Chicken are created with a lower limit of zero
x1 = LpVariable("ChickenPercent", 0, None, LpInteger)
x2 = LpVariable("BeefPercent", 0, None, LpInteger)

# The objective function is added to 'prob' first
prob += 0.013 * x1 + 0.008 * x2, "Total Cost of Ingredients per can"

# The five constraints are entered
prob += x1 + x2 == 100, "PercentagesSum"
prob += 0.100 * x1 + 0.200 * x2 >= 8.0, "ProteinRequirement"
prob += 0.080 * x1 + 0.100 * x2 >= 6.0, "FatRequirement"
prob += 0.001 * x1 + 0.005 * x2 <= 2.0, "FibreRequirement"
prob += 0.002 * x1 + 0.005 * x2 <= 0.4, "SaltRequirement"

# The problem data is written to an .lp file
# prob.writeLP("WhiskasModel.lp")

# list available solvers
print("Solvers")
solver_list = pl.listSolvers(onlyAvailable=True)
solver = pl.getSolver('GLPK_CMD')

# The problem is solved using PuLP's choice of Solver
prob.solve(solver)

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)