import numpy as np
import pandas as pd
from datetime import datetime


csv_file = r"C:\Users\User\digitalizare\dirty_cafe_sales.csv"
target_file = r"C:\Users\User\digitalizare\transformed_data.csv" 

def extract_from_csv(file_path): 
    df = pd.read_csv(file_path) 
    return df

  
def transform(df): 
    
    df.columns = df.columns.str.strip()
    cols_to_fix = ['Quantity', 'Unit_Price', 'Total']
    for col in cols_to_fix:
        if col in df.columns:
           
            df[col] = df[col].astype(str).str.replace('$', '', regex=False).str.strip()

            
            df[col] = pd.to_numeric(df[col], errors='coerce')

            
            df[col] = df[col].fillna(0)

   
    cols_to_fix = ['Quantity', 'Unit_Price', 'Total']
    zeros_per_row = (df[cols_to_fix] == 0).sum(axis=1)
    df = df[zeros_per_row <= 2]


    
    if set(cols_to_fix).issubset(df.columns):
        
       
        col_q = (df['Quantity'] == 0) & (df['Total'] != 0) & (df['Unit_Price'] != 0)
        df.loc[col_q , 'Quantity'] = df.loc[col_q , 'Total'] / df.loc[col_q , 'Unit_Price']

        
        col_p = (df['Unit_Price'] == 0) & (df['Total'] != 0) & (df['Quantity'] != 0)
        df.loc[col_p, 'Unit_Price'] = df.loc[col_p, 'Total'] / df.loc[col_p, 'Quantity']

        
        col_t = (df['Quantity'] != 0) & (df['Unit_Price'] != 0)
        df.loc[col_t, 'Total'] = df.loc[col_t, 'Quantity'] * df.loc[col_t, 'Unit_Price']

        
        df['Unit_Price'] = df['Unit_Price'].round(2)
        df['Total'] = df['Total'].round(2)
        df['Quantity'] = df['Quantity'].round(2)

    
    df['Item'] = df['Item'].astype(str)
    
    menu_rules = {
            1.0: 'Cookie',
            1.5: 'Tea',  
            2.0: 'Coffee',
            5.0: 'Salad'
        }
    for unit_price, item in menu_rules.items():
            col_i = np.isclose(df['Unit_Price'], unit_price)
            df.loc[col_i, 'Item'] = item
   
    conditional_rules = {
            3.0: 'Unknown',
            4.0: 'Unknown'
        }

    col_i_bad_item = df['Item'].str.contains(r'(?i)\b(ERROR|UNKNOWN|nan)\b', regex=True) | (df['Item'].str.strip() == '')
        
    for price, item_name in conditional_rules.items():
            
            mask_cond = np.isclose(df['Unit_Price'], price) & col_i_bad_item
            
            
            df.loc[mask_cond, 'Item'] = item_name


   
    text_cols_unknown = ['Location', 'Payment_Method'] 
    
    for col in text_cols_unknown:
        if col in df.columns:
            df[col] = df[col].astype(str)
            
            df[col] = df[col].str.replace(r'(?i)\b(error|unknown|nan)\b', 'UNKNOWN', regex=True)
            
            df[col] = df[col].replace(['', ' '], 'UNKNOWN')
            
            df[col] = df[col].str.strip().str.title()
        
    
    if 'Date' in df.columns:
        
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
        
        default_date = pd.Timestamp('2000-12-31')
        
        df['Date'] = df['Date'].fillna(default_date)


    df = df.drop_duplicates()
    
    if 'Transaction ID' in df.columns:
        df = df.dropna(subset=['Transaction ID'])

    df = df.reset_index(drop=True)
    return df
   



def load_data(df, target_file): 
    df.to_csv(target_file, index=False)
    print("Data cleaning complete. Cleaned data saved to:", target_file)
    

df = extract_from_csv(csv_file)

df = transform(df)

load_data(df, target_file)
