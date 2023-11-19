import numpy as np
from scipy.optimize import minimize
from requirements import entry_level_specs, advanced_level_specs, premium_level_specs, initial_capital
from constraints import budget_constraint, maintenance_constraint

# Define the objective function (e.g., minimize total cost)
def objective(x):
    return np.dot(x, [entry_level_specs['cost'], advanced_level_specs['cost'], premium_level_specs['cost']])

# Initial guesses
x0 = np.array([1, 1, 1])

# Define the bounds for each variable (e.g., you cannot have negative machines)
bounds = [(0, None), (0, None), (0, None)]

# Define the constraints
constraints = [{'type': 'ineq', 'fun': budget_constraint},
               {'type': 'ineq', 'fun': maintenance_constraint}]

# Run the optimization
solution = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

# Output the results
if solution.success:
    print('Optimal number of machines:', solution.x)
    print('Total cost:', objective(solution.x))
else:
    print('Optimization did not converge')
