import pandas as pd
import glob

# Step 1: Load all CSVs from the data folder
files = glob.glob("data/daily_sales_data_*.csv")
df_list = []

for file in files:
    df = pd.read_csv(file)
    
    # Step 2: Keep only Pink Morsels
    df = df[df["product"] == "pink morsel"]
    
    # Step 3: Create sales column (quantity * price)
    df["sales"] = df["quantity"] * df["price"]
    
    # Step 4: Keep only relevant columns
    df = df[["sales", "date", "region"]]
    
    df_list.append(df)

# Step 5: Combine into one dataframe
final_df = pd.concat(df_list)

# Step 6: Save to CSV
final_df.to_csv("sales.csv", index=False)

print("✅ Processed data saved to sales.csv")
