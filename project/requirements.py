# MRI Machine Specifications
entry_level_specs = {
    'cost': 150000,
    'maintenance_downtime': 30,  # in hours
    'maintenance_frequency': 4,  # times per year
    'service_rate': 300          # per hour
}

advanced_level_specs = {
    'cost': 375000,
    'maintenance_downtime': 40,
    'maintenance_frequency': 6,
    'service_rate': 500
}

premium_level_specs = {
    'cost': 400000,
    'maintenance_downtime': 60,
    'maintenance_frequency': 8,
    'service_rate': 600
}

# Operational Data
scans_per_year = {
    'entry_level': 6165,
    'advanced_level': 6165,  # Assuming same for simplicity, adjust as needed
    'premium_level': 6165
}

# Budget
initial_capital = 30000  # $30,000
