from requirements import MRI_machine_specs
from optimization import ddp_mri_optimization
from classes import Hospital

revenue_per_hour = 1000
operational_lifespan = {'entry_level': 5, 'advanced_level': 7, 'premium_level': 10}
num_machines = 3
planning_horizon = 10

hospital = Hospital(MRI_machine_specs, revenue_per_hour, operational_lifespan)
optimal_sequence, total_net_revenue = hospital.ddp_optimization(planning_horizon, num_machines)

print("Optimal Purchase Sequence:", optimal_sequence)
print("Total Net Revenue:", total_net_revenue)

decision_sequence = hospital.create_decision_sequence(optimal_sequence)
machine_sequence = hospital.create_machine_sequence(optimal_sequence)

hospital.plot_decision_tree(decision_sequence)
hospital.plot_checkerboard(machine_sequence)