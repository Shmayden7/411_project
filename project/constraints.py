from requirements import entry_level_specs, advanced_level_specs, premium_level_specs, initial_capital

def budget_constraint(x):
    total_cost = (x[0] * entry_level_specs['cost'] + 
                  x[1] * advanced_level_specs['cost'] + 
                  x[2] * premium_level_specs['cost'])
    return initial_capital - total_cost  # This should be non-negative

def maintenance_constraint(x):
    # Example: Total maintenance downtime for all machines should be within a limit
    total_downtime = (x[0] * entry_level_specs['maintenance_downtime'] + 
                      x[1] * advanced_level_specs['maintenance_downtime'] + 
                      x[2] * premium_level_specs['maintenance_downtime'])
    max_downtime = 100  # Define a reasonable maximum downtime
    return max_downtime - total_downtime
