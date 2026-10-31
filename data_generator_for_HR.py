import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker and set seed for reproducibility
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

NUM_EMPLOYEES = 800
START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2023, 12, 31)

print("Generating Employees...")
departments = ['Sales', 'Engineering', 'Support', 'Marketing', 'HR']
regions = ['North America', 'EMEA', 'APAC']

employees = []
for i in range(1, NUM_EMPLOYEES + 1):
    emp_id = f"EMP-{i:04d}"
    hire_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
    dept = np.random.choice(departments, p=[0.35, 0.25, 0.20, 0.15, 0.05])

    employees.append({
        "Employee_ID": emp_id,
        "First_Name": fake.first_name(),
        "Last_Name": fake.last_name(),
        "Department": dept,
        "Region": random.choice(regions),
        "Manager_ID": f"MGR-{random.randint(1, 50):03d}",
        "Hire_Date": hire_date,
        "Annual_Salary": round(np.random.normal(loc=75000, scale=15000), -3)  # Mean 75k, rounded
    })

df_emp = pd.DataFrame(employees)

print("Generating Performance Reviews...")
reviews = []
review_id_counter = 1

for _, emp in df_emp.iterrows():
    # 2 to 4 reviews per employee
    num_reviews = random.randint(2, 4)
    for _ in range(num_reviews):
        rev_date = fake.date_between(start_date=emp["Hire_Date"], end_date=END_DATE)

        # Pattern 1: Q4 Seasonal Dip in Ratings
        base_rating = np.random.normal(loc=3.5, scale=0.8)
        if rev_date.month in [10, 11, 12]:
            base_rating -= 0.6

        rating = max(1, min(5, round(base_rating)))  # Clamp between 1 and 5

        reviews.append({
            "Review_ID": f"REV-{review_id_counter:05d}",
            "Employee_ID": emp["Employee_ID"],
            "Review_Date": rev_date,
            "Overall_Rating": rating,
            "Productivity_Score": max(40, min(100, int(rating * 20 + random.randint(-10, 10)))),
            "Quality_Score": max(40, min(100, int(rating * 20 + random.randint(-10, 10))))
        })
        review_id_counter += 1

df_rev = pd.DataFrame(reviews)

print("Generating PIP Cases...")
pip_cases = []
pip_id_counter = 1
reasons = ['Quality of Work', 'Attendance', 'Sales Targets', 'Conduct']

# Convert END_DATE to a date object for clean date math
end_date_obj = END_DATE.date()

for _, emp in df_emp.iterrows():
    # Pattern 2: Sales dept has a much higher chance of getting a PIP
    pip_prob = 0.25 if emp["Department"] == 'Sales' else 0.10

    if random.random() < pip_prob:
        min_start = emp["Hire_Date"] + timedelta(days=90)
        max_start = end_date_obj - timedelta(days=60)

        # Skip PIP generation if the employee hasn't been here long enough
        if min_start > max_start:
            continue

        start_date = fake.date_between(start_date=min_start, end_date=max_start)
        end_date = start_date + timedelta(days=random.choice([30, 60, 90]))

        tenure_at_pip = (start_date - emp["Hire_Date"]).days

        # Pattern 3: Newer hires (< 1 year) fail PIPs much more frequently
        if tenure_at_pip < 365:
            outcome = np.random.choice(['Terminated', 'Resigned', 'Retained'], p=[0.5, 0.3, 0.2])
        else:
            outcome = np.random.choice(['Terminated', 'Resigned', 'Retained'], p=[0.1, 0.1, 0.8])

        pip_cases.append({
            "Case_ID": f"PIP-{pip_id_counter:04d}",
            "Employee_ID": emp["Employee_ID"],
            "Start_Date": start_date,
            "End_Date": end_date,
            "Reason_Category": 'Sales Targets' if emp["Department"] == 'Sales' else random.choice(reasons),
            "Status": "Completed",
            "Outcome": outcome
        })
        pip_id_counter += 1

df_pip = pd.DataFrame(pip_cases)

print("Generating PIP Milestones...")
milestones = []
ms_id_counter = 1

for _, pip in df_pip.iterrows():
    num_milestones = 3
    days_between = (pip["End_Date"] - pip["Start_Date"]).days // num_milestones

    for i in range(1, num_milestones + 1):
        check_date = pip["Start_Date"] + timedelta(days=days_between * i)

        # Tie milestone success to the final outcome
        if pip["Outcome"] == 'Retained':
            ms_status = np.random.choice(['Met', 'Not Met'], p=[0.8, 0.2])
        else:
            ms_status = np.random.choice(['Met', 'Not Met'], p=[0.3, 0.7])

        milestones.append({
            "Milestone_ID": f"MS-{ms_id_counter:05d}",
            "Case_ID": pip["Case_ID"],
            "Checkpoint_Date": check_date,
            "Target_Metric": "Weekly Goal Review",
            "Status": ms_status
        })
        ms_id_counter += 1

df_ms = pd.DataFrame(milestones)

print("Generating Date Dimension Table...")
date_range = pd.date_range(start=START_DATE, end=END_DATE)
df_dates = pd.DataFrame({
    "Date": date_range,
    "Year": date_range.year,
    "Quarter": date_range.quarter,
    "Month_Num": date_range.month,
    "Month_Name": date_range.strftime('%b'),
    "Day_of_Week": date_range.strftime('%A')
})

# Export to CSV
print("Exporting to CSV...")
df_emp.to_csv("employees.csv", index=False)
df_rev.to_csv("performance_reviews.csv", index=False)
df_pip.to_csv("pip_cases.csv", index=False)
df_ms.to_csv("pip_milestones.csv", index=False)
df_dates.to_csv("date_dim.csv", index=False)

print("✅ All 5 CSV files generated successfully!")