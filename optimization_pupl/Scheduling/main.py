import pandas as pd
import pulp

# Load Factory datasource
factories = pd.read_csv('datasource/factory_variables.csv', index_col=['Month', 'Factory'])
print(factories)

# Load demand datasource
demand = pd.read_csv('datasource/monthly_demand.csv', index_col=['Month'])
print(demand)

# We have a value for production for each month for each factory, this is given by the tuples of our multi-index
# pandas DataFrame index.
production = pulp.LpVariable.dicts("production",
                                   ((month, factory) for month, factory in factories.index),
                                   lowBound=0,
                                   cat='Integer')

# Again this has a value for each month for each factory, again given by the index of our DataFrame
factory_status = pulp.LpVariable.dicts("factory_status",
                                       ((month, factory) for month, factory in factories.index),
                                       cat='Binary')

# We instantiate our model and use LpMinimize as the aim is to minimise costs.
model = pulp.LpProblem("Cost minimising scheduling problem", pulp.LpMinimize)

# In our objective function we include our 2 costs:
model += pulp.lpSum(
  [production[month, factory] * factories.loc[(month, factory), 'Variable_Costs'] for month, factory in factories.index]
+ [factory_status[month, factory] * factories.loc[(month, factory), 'Fixed_Costs'] for month, factory in factories.index]
)

# Our variable costs is the product of the variable costs per unit and production
# Our fixed costs is the factory status – 1 (on) or 0 (off) – multiplied by the fixed cost of production

# Production in any month must be equal to demand
months = demand.index
for month in months:
    model += production[(month, 'A')] + production[(month, 'B')] == demand.loc[month, 'Demand']

# Factory B is off in May
model += factory_status[5, 'B'] == 0
model += production[5, 'B'] == 0

# Production in any month must be between minimum and maximum capacity, or zero.
for month, factory in factories.index:
    min_production = factories.loc[(month, factory), 'Min_Capacity']
    max_production = factories.loc[(month, factory), 'Max_Capacity']
    model += production[(month, factory)] >= min_production * factory_status[month, factory]
    model += production[(month, factory)] <= max_production * factory_status[month, factory]

# We then solve the model
model.solve()
pulp.LpStatus[model.status]

# Let’s take a look at the optimal production schedule output for each month from each factory. For ease of viewing
# we’ll output the data to a pandas DataFrame.
output = []
for month, factory in production:
    var_output = {
        'Month': month,
        'Factory': factory,
        'Production': production[(month, factory)].varValue,
        'Factory Status': factory_status[(month, factory)].varValue
    }
    output.append(var_output)
output_df = pd.DataFrame.from_records(output).sort_values(['Month', 'Factory'])
output_df.set_index(['Month', 'Factory'], inplace=True)
print(output_df)

# Print our objective function value (Total Costs)
print("Minimum Total Cost = {}".format(pulp.value(model.objective)))
