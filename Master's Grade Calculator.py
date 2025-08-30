import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- CONFIGURATION ---
# Set to True to include Year 4 (Masters), False for Bachelors only
include_masters = True
desired_final_grade = 70  # Your target overall grade (e.g., 70 for a First)

# --- YOUR GRADES AND MODULE WEIGHTS ---
# Note: For incomplete modules, set the grade to None

# === YEAR 2 ===
# (Assumed to be fully complete)
year2_weights = {
    "Aero1": 10/120, "Aero2": 10/120, "MATLAB": 10/120, "PPM": 20/120,
    "MDM2_Reflection": 0.1*(20/120), "MDM2_IP1": 0.1*(20/120), "MDM2_P1": 0.25*(20/120),
    "MDM2_P2": 0.25*(20/120), "MDM2_P3": 0.3*(20/120), "Discrete_CW1": 0.05*(10/120),
    "Discrete_CW2": 0.05*(10/120), "Discrete_CW3": 0.05*(10/120), "ALA_CW1": 0.05*(10/120),
    "ALA_CW2": 0.05*(10/120), "ALA_CW3": 0.05*(10/120), "Eng_maths": 20/120,
    "ALA": 0.85*(10/120), "Data_Science": 10/120, "Discrete": 0.85*(10/120)
}
year2_grades = {
    "Aero1": 67, "Aero2": 68, "MATLAB": 88, "PPM": 79, "MDM2_Reflection": 89,
    "MDM2_IP1": 71, "MDM2_P1": 70, "MDM2_P2": 69, "MDM2_P3": 58, "Discrete_CW1": 92,
    "Discrete_CW2": 88, "Discrete_CW3": 100, "ALA_CW1": 80, "ALA_CW2": 96,
    "ALA_CW3": 88, "Eng_maths": 62, "ALA": 68, "Data_Science": 81, "Discrete": 80
}

# === YEAR 3 ===
year3_weights = {
    "SCO": 20/120, "Data_Science_2": 20/120, "MDM3_P1": 12/120, "MDM3_P2": 12/120,
    "MDM3_P3": 8/120, "MDM3_PPP": 8/120, "MoAM": 20/120, "MoAI": 20/120
}
# This is the corrected dictionary with all modules completed
year3_grades = {
    "SCO": 71.66, "Data_Science_2": 71, "MDM3_P1": 65.6, "MDM3_P2": 65.5,
    "MDM3_P3": 71.65, "MDM3_PPP": 71.65, "MoAM": 86, "MoAI": 85
}

# === YEAR 4 ===
# (Only used if include_masters is True)
year4_weights = {
    "Project_Part1": 15/120,
    "Project_Part2": 45/120,
    "Advanced_ML": 20/120,
    "Quantum_Computing": 20/120,
    "Another_Module": 20/120,
}
year4_grades = {
    "Project_Part1": None,
    "Project_Part2": None,
    "Advanced_ML": None,
    "Quantum_Computing": None,
    "Another_Module": None,
}

# --- CALCULATIONS ---

# 1. Set degree weights based on the toggle
if include_masters:
    year_w = {'y2': 0.1, 'y3': 0.4, 'y4': 0.5}
    degree_type = "Integrated Master's"
else:
    year_w = {'y2': 0.25, 'y3': 0.75, 'y4': 0.0}
    degree_type = "Bachelor's"

# 2. Define a function to calculate weighted average for a year
def calculate_year_grade(weights, grades):
    """
    Calculates the weighted average grade for a given set of completed modules.
    'grades' should be a dictionary containing only the modules with grades.
    """
    # Calculate the sum of weights ONLY for the modules that have grades
    total_weight = sum(weights[m] for m in grades)

    # Calculate the weighted sum of grades
    total_sum = sum(weights[m] * grades[m] for m in grades)

    # Return the average, handling the case of no completed modules
    return total_sum / total_weight if total_weight > 0 else 0

# 3. Calculate overall grade for each year
year2_final_grade = calculate_year_grade(year2_weights, year2_grades)
year3_final_grade = calculate_year_grade(year3_weights, {k: v for k, v in year3_grades.items() if v is not None})
year4_final_grade = calculate_year_grade(year4_weights, {k: v for k, v in year4_grades.items() if v is not None})

# 4. Calculate current overall grade and required grade for the target
total_weighted_sum = 0.0
total_completed_weight = 0.0
total_remaining_weight = 0.0

# Year 2 contribution (fully complete)
total_weighted_sum += year2_final_grade * year_w['y2']
total_completed_weight += year_w['y2']

# Year 3 contribution
for module, weight in year3_weights.items():
    grade = year3_grades.get(module)
    if grade is not None:
        total_weighted_sum += grade * weight * year_w['y3']
        total_completed_weight += weight * year_w['y3']
    else:
        total_remaining_weight += weight * year_w['y3']

# Year 4 contribution (if applicable)
if include_masters:
    for module, weight in year4_weights.items():
        grade = year4_grades.get(module)
        if grade is not None:
            total_weighted_sum += grade * weight * year_w['y4']
            total_completed_weight += weight * year_w['y4']
        else:
            total_remaining_weight += weight * year_w['y4']

current_overall_grade = total_weighted_sum / total_completed_weight if total_completed_weight > 0 else 0
needed_avg_on_remaining = (desired_final_grade - total_weighted_sum) / total_remaining_weight if total_remaining_weight > 0 else float('inf')

# --- ANALYSIS & OUTPUT ---
print("-" * 50)
print(f"DEGREE PROGRESS ANALYSIS ({degree_type})")
print("-" * 50)
print(f"Year 2 Final Grade: {year2_final_grade:.2f}")
print(f"Year 3 Current Grade (based on completed modules): {year3_final_grade:.2f}")
if include_masters:
    print(f"Year 4 Current Grade (based on completed modules): {year4_final_grade:.2f}")

print("\n--- OVERALL STATUS ---")
print(f"Current Overall Degree Grade: {current_overall_grade:.2f}")
print(f"Target Grade: {desired_final_grade}")

if total_remaining_weight > 0:
    print(f"\nTo achieve an overall grade of {desired_final_grade}, you need an average of:")
    print(f"  -> {needed_avg_on_remaining:.2f} <-")
    print("across all remaining modules.")
else:
    print("\nAll modules are complete. No further calculations needed.")

print("-" * 50)

# --- VISUALISATIONS ---
sns.set_theme(style="whitegrid")

# 1. Plot Module Performance
all_grades = {f"Y2: {k}": v for k, v in year2_grades.items()}
all_grades.update({f"Y3: {k}": v for k, v in year3_grades.items() if v is not None})
if include_masters:
    all_grades.update({f"Y4: {k}": v for k, v in year4_grades.items() if v is not None})

plt.figure(figsize=(12, 10))
sns.barplot(x=list(all_grades.values()), y=list(all_grades.keys()), palette="viridis")
plt.title("Performance by Module", fontsize=16)
plt.xlabel("Grade Achieved")
plt.ylabel("Module")
plt.axvline(x=70, color='r', linestyle='--', label='First Class Boundary (70)')
plt.axvline(x=60, color='orange', linestyle='--', label='2:1 Boundary (60)')
plt.legend()
plt.tight_layout()
plt.show()

# 2. Plot Overall Grade Contribution
contributions = {
    'Year 2': year2_final_grade * year_w['y2'],
    'Year 3 (Completed)': year3_final_grade * sum(w for m, w in year3_weights.items() if year3_grades.get(m) is not None) * year_w['y3']
}
if include_masters:
    contributions['Year 4 (Completed)'] = year4_final_grade * sum(w for m, w in year4_weights.items() if year4_grades.get(m) is not None) * year_w['y4']

plt.figure(figsize=(10, 6))
sns.barplot(x=list(contributions.keys()), y=list(contributions.values()), palette="crest")
plt.title("Contribution to Current Overall Grade", fontsize=16)
plt.ylabel("Weighted Grade Points")
for index, value in enumerate(contributions.values()):
    plt.text(index, value + 0.5, f"{value:.2f}", ha="center")
plt.ylim(0, max(contributions.values()) * 1.2)
plt.show()

# 3. Plot "What-If" Scenario for Remaining Modules
if total_remaining_weight > 0:
    x_what_if = np.linspace(40, 100, 100) # Potential average grades for remaining modules
    y_final_grade = total_weighted_sum + (x_what_if * total_remaining_weight)

    plt.figure(figsize=(10, 6))
    plt.plot(x_what_if, y_final_grade, label="Projected Final Grade")
    plt.axhline(y=70, color='r', linestyle='--', label='First Class (70)')
    plt.axhline(y=60, color='orange', linestyle='--', label='Upper Second (2:1, 60)')
    plt.axhline(y=50, color='y', linestyle='--', label='Lower Second (2:2, 50)')
    plt.axvline(x=needed_avg_on_remaining, color='g', linestyle=':', label=f'Needed for {desired_final_grade} ({needed_avg_on_remaining:.2f})')

    plt.title("What-If Analysis: Final Grade vs. Remaining Module Performance", fontsize=16)
    plt.xlabel("Average Grade Achieved in Remaining Modules")
    plt.ylabel("Resulting Final Degree Grade")
    plt.legend()
    plt.grid(True)
    plt.show()