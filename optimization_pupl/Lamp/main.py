# from pulp import *
import pulp

# Create the 'prob' variable to contain the problem data
prob = pulp.LpProblem("The_Lamp_Problem", pulp.LpMaximize)

# The 2 variables L1 and L2 model lamps created with a lower limit of zero (constrains)
L1 = pulp.LpVariable("L1", 0, None, pulp.LpInteger)
L2 = pulp.LpVariable("L2", 0, None, pulp.LpInteger)

# The objective function is added to 'prob' first
prob += 16 * L1 + 10 * L2, "Maximum profit"

# The two constraints are entered
prob += 1/3 * L1 + 1/2 * L2 <= 100, "Manual hours"
prob += 1/3 * L1 + 1/6 * L2 <= 80, "Machine hours"

# The problem is solved using PuLP's choice of Solver
prob.solve()

# print status resolver
print(pulp.LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)
