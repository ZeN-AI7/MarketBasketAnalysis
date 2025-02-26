import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# 1. Load the Excel data (using openpyxl)
df = pd.read_excel("/Users/zen/Documents/Datasets for ML/Online Retail.xlsx", engine='openpyxl')
print("Data loaded successfully. Preview:")
(df.head())

# 2. Data Cleaning
df_clean = df.dropna(subset=['InvoiceNo', 'Description'])
df_clean = df_clean[df_clean['Quantity'] > 0]
df_clean['InvoiceNo'] = df_clean['InvoiceNo'].astype(str)
df_clean['Description'] = df_clean['Description'].str.strip()
print("\nData cleaning complete. Preview:")
(df_clean.head())

# 3. Create the Basket (Pivot the Data)
basket = df_clean.groupby(['InvoiceNo', 'Description'])['Quantity'].sum().unstack().fillna(0)
print("\nBasket created. Shape:", basket.shape)
(basket.head())

# 4. One-Hot Encoding: Convert quantities to binary (1 if purchased, 0 otherwise)
basket_encoded = basket.applymap(lambda x: 1 if x >= 1 else 0)
print("\nBasket encoded for Market Basket Analysis:")
(basket_encoded.head())

# 5. Run the Apriori Algorithm to find frequent itemsets
# Adjust the min_support threshold to capture more frequent itemsets (e.g., 0.01)
min_support_threshold = 0.01
frequent_itemsets = apriori(basket_encoded, min_support=min_support_threshold, use_colnames=True)
print(f"\nFrequent itemsets generated with min_support={min_support_threshold}. Shape:", frequent_itemsets.shape)
(frequent_itemsets.head())

# Check if any frequent itemsets were found
if frequent_itemsets.empty:
    print("No frequent itemsets found. Consider lowering the min_support threshold further.")
else:
    # 6. Generate Association Rules based on the frequent itemsets
    # Option: Adjust min_threshold for lift or consider using 'confidence' metric instead
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    print("\nAssociation rules generated. Shape:", rules.shape)
    (rules.head())

    # Save the rules to a CSV file if they exist
    if not rules.empty:
        rules.to_csv("/Users/zen/Documents/Datasets for ML/association_rules.csv", index=False)
        print("\nAssociation rules saved successfully.")
    else:
        print("No association rules generated. Try adjusting the thresholds.")
