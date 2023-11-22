from itertools import product
import matplotlib.pyplot as plt
import numpy as np

class MRI:
    def __init__(self, name, cost, maintenance_downtime, maintenance_frequency, service_rate):
        self.name = name
        self.cost = cost
        self.maintenance_downtime = maintenance_downtime
        self.maintenance_frequency = maintenance_frequency
        self.service_rate = service_rate

class Hospital:
    def __init__(self, mri_specs, revenue_per_hour, operational_lifespan):
        self.mris = {name: MRI(name, **specs) for name, specs in mri_specs.items()}
        self.revenue_per_hour = revenue_per_hour
        self.operational_lifespan = operational_lifespan
        self.memo = {} # memoization dictionary

    def calculate_annual_net_revenue(self, mri, year):
        if year >= self.operational_lifespan[mri.name]:
            return -float('inf')
        annual_revenue = self.revenue_per_hour * (365 * 24 - mri.maintenance_downtime * mri.maintenance_frequency)
        annual_cost = mri.cost * (year == 0)
        return annual_revenue - annual_cost

    def ddp_optimization(self, horizon, num_machines):
            def optimize(year, current_machines):
                # Check if the computation has already been done
                memo_key = (year, current_machines)
                if memo_key in self.memo:
                    return self.memo[memo_key]

                if year == horizon:
                    return [], 0

                best_sequence = None
                best_net_revenue = -float('inf')

                for machine_combination in product(self.mris.keys(), repeat=num_machines):
                    sequence, net_revenue = optimize(year + 1, machine_combination)
                    net_revenue += sum(self.calculate_annual_net_revenue(self.mris[machine_type], year if machine_type == current_machines[i] else 0) for i, machine_type in enumerate(machine_combination))

                    if net_revenue > best_net_revenue:
                        best_net_revenue = net_revenue
                        best_sequence = [machine_combination] + sequence
                
                # Store the result in the memo before returning
                self.memo[memo_key] = (best_sequence, best_net_revenue)
                return best_sequence, best_net_revenue

            # Clear the memoization cache before starting
            self.memo.clear()
            return optimize(0, (None,) * num_machines)
     
    def create_decision_sequence(self, optimal_sequence):
        decision_sequence = []
        for i in range(1, len(optimal_sequence)):
            year_decisions = optimal_sequence[i]
            previous_year_decisions = optimal_sequence[i - 1]
            yearly_decision = []

            for j in range(len(year_decisions)):
                if year_decisions[j] == previous_year_decisions[j]:
                    yearly_decision.append('Keep')
                else:
                    yearly_decision.append('Replace')

            decision_sequence.append(yearly_decision)
        return decision_sequence
    
    def create_machine_sequence(self, optimal_sequence):
        # This method should transform the optimal sequence of tuples into a sequence of machine types
        machine_sequence = []
        for year in optimal_sequence:
            # Extract the machine type from each tuple in the year
            machine_sequence.append([machine[0] for machine in year])  # Assume machine type is the first element in the tuple
        return machine_sequence

    def plot_decision_tree(self, decision_sequence, title='MRI Equipment Decision Tree'):
        # Set up the figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Starting point for the plot
        current_age = 0
        current_time = 0

        # Plot the decision points and paths
        for decisions in decision_sequence:
            for decision in decisions:
                next_age = current_age + 1 if decision == 'Keep' else 0
                next_time = current_time + 1
                
                # Plot the current equipment age (Defender)
                ax.plot([current_time, next_time], [current_age, next_age], '-o', label='Keep' if current_time == 0 else "")
                
                # If the decision is to replace, plot the replacement (Challenger)
                if decision == 'Replace':
                    ax.plot([current_time, next_time], [current_age, 0], '--o', label='Replace' if current_time == 0 else "")
                
                current_age = next_age
            current_time = next_time
            current_age = 0  # Reset for the next machine

        # Set the plot title and labels
        ax.set_title(title)
        ax.set_xlabel('Horizon (Time)')
        ax.set_ylabel('Equipment Age')
        
        # Remove duplicate labels
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())

        # Show the plot
        plt.show()

    def plot_checkerboard(self, machine_sequence):
        # Define symbols for each type of MRI machine
        symbols = {
            'e': 'E',  # Symbol for entry level MRI machine
            'a': 'A',  # Symbol for advanced level MRI machine
            'p': 'P'  # Symbol for premium level MRI machine
        }

        # Determine the grid size
        num_years = len(machine_sequence)
        num_machines = len(machine_sequence[0])

        # Create a grid for the checkerboard
        grid = np.zeros((num_years, num_machines), dtype=str)

        # Populate the grid with the symbols
        for year, machine_types in enumerate(machine_sequence):
            for machine_index, machine_type in enumerate(machine_types):
                grid[year, machine_index] = symbols[machine_type]

        # Plotting the checkerboard
        fig, ax = plt.subplots()
        ax.table(cellText=grid, loc='center', cellLoc='center')
        
        # Adjust layout for better fit
        ax.axis('tight')
        ax.axis('off')
        plt.grid()

        # Adding labels for clarity
        plt.xlabel('MRI Machines')
        plt.ylabel('Years')

        plt.title('MRI Machine Types Over Time')

        # Display the plot
        plt.show()