# HR Analytics & PIP Tracker (PowerBI)

An end-to-end HR analytics project in Power BI that tracks Performance Improvement Plans (PIPs), employee retention and manager effectiveness. The data model follows a star schema, the measures are written in DAX, and the dataset is **fully synthetic**, generated with Python, so no real employee information is used.

![Dashboard overview](images/dashboard-overview.png)

## The business problem

HR teams need to know whether Performance Improvement Plans are working. Which departments and regions place the most employees on PIPs? How often do PIPs end in a retained, resigned or terminated employee? Are checkpoints being met along the way? Without a single view, these answers sit in separate spreadsheets and are slow to produce.

This dashboard brings reviews, PIP cases and milestones into one model so HR and managers can monitor performance and retention in a self-service way.

## What the project includes

|File / folder|Purpose|
|-|-|
|`HR-Data_Analytics_PIP.pbix`|The Power BI report (data model, DAX measures and visuals)|
|`data_generator_for_HR.py`|Python script that generates the synthetic datasets|
|`Sample Employee Data/`|Sample CSV output from the generator, used as the report’s source|
|[`HR-Data_Analytics_PIP 2026-10-31 15-21-09.mp4`](HR-Data_Analytics_PIP%202026-10-31%2015-21-09.mp4)|Screen recording walking through the dashboard|

## Synthetic data

`data_generator_for_HR.py` uses `pandas`, `numpy` and `Faker` (with fixed seeds, so results are reproducible) to create **800 employees** hired between 2020 and 2023, and exports five CSV files:

|Table|Description|
|-|-|
|`employees.csv`|Employee ID, name, department, region, manager ID, hire date, annual salary|
|`performance_reviews.csv`|2 to 4 reviews per employee with overall rating, productivity and quality scores|
|`pip_cases.csv`|PIP start and end dates, reason category and outcome (Retained, Resigned or Terminated)|
|`pip_milestones.csv`|Three checkpoints per PIP with a Met / Not Met status|
|`date_dim.csv`|Date dimension (year, quarter, month, day of week)|

### Patterns built into the data

Real HR data is not shared publicly, so the generator plants realistic patterns for the dashboard to uncover:

* **Sales has a higher PIP rate:** 25% of Sales employees are placed on a PIP, against 10% elsewhere.
* **New hires struggle more:** employees with under a year of tenure at the time of the PIP are far more likely to be terminated or to resign.
* **Milestones predict outcomes:** employees who are retained meet most checkpoints, while those who leave miss most of them.
* **Q4 rating dip:** performance review ratings are lower in October to December.

Because these patterns are planted, the findings show what the dashboard can surface. They are not claims about any real organisation.

## Data model

![Data model](images/data-model.png)

The model uses a star schema:

* **Dimension tables:** `employees` and `date_dim`
* **Fact tables:** `performance_reviews`, `pip_cases` and `pip_milestones`
* Employees link to reviews and PIP cases through `Employee_ID`, PIP milestones link to PIP cases through `Case_ID`, and dates link through a date relationship.

## Dashboard features

* Multi-page report built with card visuals and slicers
* Custom DAX measures for PIP rate, outcome rates and milestone completion
* Breakdowns by department, region and manager
* Trend analysis over time using the date dimension

## How to run it

1. Install the requirements: `pip install pandas numpy faker`
2. Generate the data: `python data_generator_for_HR.py`
3. Open `HR-Data_Analytics_PIP.pbix` in Power BI Desktop and refresh (update the data source path to your CSV folder if prompted).

## Skills demonstrated

Power BI Desktop, DAX, star schema data modelling, Python (pandas, NumPy, Faker), synthetic data generation, KPI design, HR and people analytics, data storytelling.
