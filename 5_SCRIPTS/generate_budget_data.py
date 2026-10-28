"""
generate_budget_data.py
Creates a SIMULATED monthly budget vs actual dataset for a fictional company,
"Brightline Retail Ltd", for January to December 2025.
The data is made up for practice. It is not real company data.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)          # fixed seed so the numbers are repeatable
months = pd.date_range("2025-01-01", "2025-12-01", freq="MS")

# Department, category, type, monthly budget (EUR)
lines = [
    ("Sales",      "Product Revenue",   "Revenue", 420000),
    ("Sales",      "Service Revenue",   "Revenue",  60000),
    ("Sales",      "Salaries",          "Expense",  85000),
    ("Sales",      "Travel",            "Expense",  12000),
    ("Marketing",  "Advertising",       "Expense",  45000),
    ("Marketing",  "Events",            "Expense",  10000),
    ("Marketing",  "Salaries",          "Expense",  30000),
    ("Operations", "Warehouse Rent",    "Expense",  40000),
    ("Operations", "Logistics",         "Expense",  55000),
    ("Operations", "Salaries",          "Expense",  70000),
    ("IT",         "Software Licences", "Expense",  18000),
    ("IT",         "Hardware",          "Expense",   8000),
    ("IT",         "Salaries",          "Expense",  35000),
    ("HR",         "Recruitment",       "Expense",   6000),
    ("HR",         "Training",          "Expense",   5000),
    ("HR",         "Salaries",          "Expense",  20000),
    ("Finance",    "Audit & Legal",     "Expense",   7000),
    ("Finance",    "Salaries",          "Expense",  25000),
]

# Seasonal pattern for revenue (busier in Q4)
season = {1: 0.85, 2: 0.85, 3: 0.95, 4: 0.95, 5: 1.00, 6: 1.00,
          7: 0.95, 8: 0.95, 9: 1.00, 10: 1.10, 11: 1.20, 12: 1.30}

rows = []
for m in months:
    for dept, cat, typ, base in lines:
        budget = base * season[m.month] if typ == "Revenue" else base
        actual = budget * rng.normal(1.0, 0.03)          # normal small differences

        # Planted business stories
        if cat == "Product Revenue" and m.month in (4, 5, 6):
            actual = budget * rng.normal(0.88, 0.02)     # weak Q2 sales
        if cat == "Advertising" and m.month in (10, 11, 12):
            actual = budget * rng.normal(1.35, 0.03)     # Q4 campaign overspend
        if cat == "Software Licences" and m.month >= 7:
            actual = budget * rng.normal(1.25, 0.02)     # new software from July
        if cat == "Travel":
            actual = budget * rng.normal(0.75, 0.05)     # travel always under budget
        if cat == "Logistics" and m.month in (11, 12):
            actual = budget * rng.normal(1.20, 0.03)     # Christmas delivery costs
        if cat == "Recruitment" and m.month in (3, 9):
            actual = budget * rng.normal(1.60, 0.05)     # two hiring drives

        rows.append({
            "Month": m.strftime("%Y-%m"),
            "Department": dept,
            "Category": cat,
            "Type": typ,
            "Budget": round(budget, 2),
            "Actual": round(actual, 2),
        })

df = pd.DataFrame(rows)
df.to_csv("budget_vs_actual_2025.csv", index=False)
print(df.shape)
