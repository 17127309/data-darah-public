# Blood Donation Data EDA

This repository contains a comprehensive Exploratory Data Analysis (EDA) of Malaysian blood donation data at both the facility (hospital) and state levels. The analysis is performed using Python and Jupyter Notebook, with clear explanations, visualizations, and actionable insights.

## Datasets
- `donations_facility.csv`: Daily blood donation records by hospital/facility.
- `donations_state.csv`: Daily blood donation records by state (excluding the national total for state-level analysis).

## EDA Highlights
- **Data Cleaning:** Date conversion, missing value handling, and exclusion of national totals for accurate state analysis.
- **Verification:** Cross-checks between facility and state datasets to ensure data consistency.
- **Descriptive Statistics:** Summary statistics for both datasets.
- **Time Series Analysis:** Monthly and yearly trends, with breakdowns by individual facility and state.
- **Distribution Analysis:** Blood type, donation type, social group, and donor type distributions.
- **Correlation Analysis:** Heatmaps for numeric columns.
- **Quadrant Analysis:** Advanced grouping of facilities and states by mean and variability of daily donations, with actionable recommendations.
- **Visualizations:** All analyses are accompanied by clear, well-labeled plots.

## How to Use
1. Clone this repository.
2. Ensure you have Python 3.x and the following packages installed:
   - pandas
   - numpy
   - matplotlib
   - seaborn
3. Open `eda_darah_public.ipynb` in Jupyter Notebook or VS Code to explore the analysis step by step.

## Reproducing the Analysis
- All code is well-commented and structured for clarity.
- The notebook is formatted for VS Code with XML-based cell markup.
- You can extend the analysis or adapt it for new data as needed.

## Authors
- Azrul Syaffiq

## Data Source
- MOH Github

## License
This project is for academic and non-commercial use. 
