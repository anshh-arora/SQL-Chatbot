import pandas as pd
import random
from datetime import datetime, timedelta

# Load the CSV file
df = pd.read_csv("Stores.csv")

# Add a Store_ID column if it doesn't already exist
if 'Store_ID' not in df.columns:
    df['Store_ID'] = range(1, len(df) + 1)

# Generate random store names
store_names = [
    "QuickMart", "FreshStop", "MegaStore", "SuperSaver", "EcoGrocer", "UrbanMart",
    "GreenBasket", "CityMarket", "PrimePick", "ValueVille"
]
df['Store_Name'] = [random.choice(store_names) for _ in range(len(df))]

# Generate random item categories
item_categories = [
    "Groceries", "Electronics", "Clothing", "Home Goods", "Toys", "Sports Equipment",
    "Beauty Products", "Books", "Pet Supplies", "Office Supplies"
]
df['Main_Category'] = [random.choice(item_categories) for _ in range(len(df))]

# Generate random popular items
popular_items = [
    "Milk", "Bread", "Eggs", "Smartphone", "T-shirt", "Bedding Set", "Action Figure",
    "Running Shoes", "Shampoo", "Bestseller Novel", "Dog Food", "Printer Paper"
]
df['Popular_Item'] = [random.choice(popular_items) for _ in range(len(df))]

# Add average transaction value
df['Avg_Transaction_Value'] = df['Store_Sales'] / df['Daily_Customer_Count']

# Add a random date for the last inventory check
start_date = datetime(2021, 1, 1)
end_date = datetime(2023, 12, 31)
df['Last_Inventory_Date'] = [start_date + timedelta(days=random.randint(0, 365)) for _ in range(len(df))]

# Add a random number of employees
df['Number_of_Employees'] = [random.randint(10, 50) for _ in range(len(df))]

# Add a random percentage of online sales
df['Online_Sales_Percentage'] = [round(random.uniform(5, 30), 2) for _ in range(len(df))]

# Calculate the estimated online sales
df['Estimated_Online_Sales'] = round(df['Store_Sales'] * df['Online_Sales_Percentage'] / 100, 2)

# Add a random customer satisfaction score
df['Customer_Satisfaction_Score'] = [round(random.uniform(3.0, 5.0), 1) for _ in range(len(df))]

# Reorder columns for better readability
column_order = [
    'Store_ID', 'Store_Name', 'Store_Area', 'Items_Available', 'Main_Category',
    'Popular_Item', 'Daily_Customer_Count', 'Store_Sales', 'Avg_Transaction_Value',
    'Online_Sales_Percentage', 'Estimated_Online_Sales', 'Last_Inventory_Date',
    'Number_of_Employees', 'Customer_Satisfaction_Score'
]
df = df[column_order]

# Display the modified DataFrame
print(df.to_string(index=False))

# Optionally, save the DataFrame to a CSV file
df.to_csv('store_data.csv', index=False)
print("\nData has been saved to 'store_data.csv'")
