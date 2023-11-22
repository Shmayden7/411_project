from itertools import product

def ddp_mri_optimization(specs, horizon, revenue_per_hour, operational_lifespan, num_machines):
    """
    Extended DDP model to determine the optimal MRI machine purchase strategy with a fixed number of machines.

    :param specs: Dictionary containing the specifications for each MRI machine type.
    :param horizon: The planning horizon in years.
    :param revenue_per_hour: Revenue generated per operational hour.
    :param operational_lifespan: Maximum operational lifespan for each MRI machine type.
    :param num_machines: Total number of MRI machines to be maintained in operation.
    :return: The optimal purchase sequence and total net revenue.
    """
    def calculate_annual_net_revenue(machine_type, year):
        machine_specs = specs[machine_type]
        if year >= operational_lifespan[machine_type]:
            return -float('inf')

        annual_revenue = revenue_per_hour * (365 * 24 - machine_specs['maintenance_downtime'] * machine_specs['maintenance_frequency']) * num_machines
        annual_cost = machine_specs['cost'] * (year == 0) * num_machines
        return annual_revenue - annual_cost

    def optimize(year, current_machines):
        if year == horizon:
            return [], 0

        best_sequence = None
        best_net_revenue = -float('inf')

        for machine_combination in product(specs.keys(), repeat=num_machines):
            sequence, net_revenue = optimize(year + 1, machine_combination)
            net_revenue += sum(calculate_annual_net_revenue(machine_type, year if machine_type == current_machines[i] else 0) for i, machine_type in enumerate(machine_combination))
            if net_revenue > best_net_revenue:
                best_net_revenue = net_revenue
                best_sequence = [machine_combination] + sequence

        return best_sequence, best_net_revenue

    return optimize(0, (None,) * num_machines)