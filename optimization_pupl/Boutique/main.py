#from pulp import *
import pulp

# Create the 'prob' variable to contain the problem data
model = pulp.LpProblem("Boutique_Profit", pulp.LpMaximize)

# The 2 variables L1 and L2 model lamps created with a lower limit of zero (contrains)
a = pulp.LpVariable("a", lowBound=0, cat='Integer')
b = pulp.LpVariable("b", lowBound=0, cat='Integer')

# The objective function is added to 'prob' first
model += 30000 * a + 45000 * b, "Maximum profit"

# The two constraints are entered
model += 3 * a + 4 * b <= 30, "Robot day time"
model += 5 * a + 6 * b <= 60, "Engineer day time"
model += 1.5 * a + 3 * b <= 21, "Detailer day time"

# The problem is solved using PuLP's choice of Solver
model.solve()

# print status resolver
print(pulp.LpStatus[model.status])

# Print our decision variable values
print("Production of Car A = {}".format(a.varValue))
print("Production of Car B = {}".format(b.varValue))

# Print our objective function value
print("Maximum Profit = {}".format(pulp.value(model.objective)))