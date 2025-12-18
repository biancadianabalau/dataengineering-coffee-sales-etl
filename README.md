
# ☕ Cafe Sales ETL & Data Cleaning Pipeline

This project contains a Python ETL (Extract, Transform, Load) script designed to clean, standardize, and transform a "dirty" dataset of cafe transactions.

The script ingests raw CSV data, applies complex cleaning rules, logically imputes missing numerical values, and exports a clean "Gold layer" dataset ready for analysis or visualization.

Data Source: The original raw dataset is available on Kaggle:  
👉 [Dirty Cafe Sales Data for Cleaning Training]  (https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training)
  
   
   How to Use

Download the dataset (dirty_cafe_sales.csv) from the link above.  
Open the Python script and update the file paths to match your local directory structure:  
Python
csv_file = r"YOUR_PATH\dirty_cafe_sales.csv"  
target_file = r"YOUR_PATH\transformed_data.csv"  
Run the script. The cleaned data will be generated as transformed_data.csv.  


 ## ⚙️ Transformation Logic (Data Cleaning)
The script performs a rigorous data cleaning process involving the following steps:

1. Initial Cleaning & Type Conversion
Column Standardization: Strips whitespace from column names.
Currency Cleaning: Removes $ symbols from Quantity, Unit_Price, and Total.
Numeric Conversion: Coerces strings to numbers; non-numeric values are filled with 0.
Row Filtering: Drops rows where Quantity, Unit_Price, and Total are all missing or zero (invalid transactions).  

2. Logical Imputation (Mathematical Recalculation)
The script uses the relationship Total = Quantity * UnitPrice to fill in missing data:
Missing Quantity: Calculated as $Total / Unit\_Price$
Missing Unit Price: Calculated as $Total / Quantity$.
Total Recalculation: Ensures consistency by recalculating the Total for all valid rows  

3. Item Mapping & CorrectionFixes invalid entries in the Item column (e.g., "ERROR", "UNKNOWN", or typos) by inferring the product based on the standardized Unit_Price:
   Price 1.0 $\rightarrow$
   CookiePrice 1.5 $\rightarrow$
   TeaPrice 2.0 $\rightarrow$
   CoffeePrice 5.0 $\rightarrow$
   Prices of 3.0 and 4.0 are explicitly marked as Unknown if the item name is invalid.  

4. Text Data Cleaning (Location & Payment)
Targets Location and Payment_Method columns.
Standardizes text using Title Case 
Uses Regex to identify variations of null values ("error", "nan", "unknown") and standardizes them to a single "UNKNOWN" label  

5. Date Handling
Converts the Date column to datetime objects (handling dayfirst format).
Coerces errors and fills missing dates with a default fallback value (2000-12-31) to maintain data integrity.  

6. Final Validation
Deduplication: Removes exact duplicate rows.
Transaction ID: Drops any rows where the Transaction ID is missing, as these are not valid records  

## 📊 Output
The output is a CSV file (transformed_data.csv) containing structured data with consistent formatting, no critical missing values, and corrected product categorizations.
