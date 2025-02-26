import streamlit as st
import pandas as pd
import ast

# Function to safely convert a frozenset string to a Python set
def parse_antecedent(x):
    # If already a frozenset, return it
    if isinstance(x, frozenset):
        return x
    # If it's a string, process it
    if isinstance(x, str):
        try:
            # Check if the string starts with "frozenset("
            if x.startswith("frozenset("):
                # Remove "frozenset(" from the start and ")" from the end
                inner_str = x[len("frozenset("):-1]
                # Now, use ast.literal_eval on the inner string
                return frozenset(ast.literal_eval(inner_str))
            else:
                # Otherwise, try directly converting
                return frozenset(ast.literal_eval(x))
        except Exception as e:
            # Log the error with the problematic value for debugging
            st.error(f"Error parsing antecedents: {e} with value: {x}")
            return frozenset()
    return frozenset()

# Set page configuration for a fun and engaging UI
st.set_page_config(
    page_title="Fun Market Basket Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🎉 Market Basket Analysis Dashboard 🎉")
st.markdown("""
Welcome to the fun and interactive Market Basket Analysis Dashboard!  
Select a product from the dropdown below to see the associated recommended items.
""")

# Sidebar information
st.sidebar.header("About This App")
st.sidebar.info("""
This dashboard visualizes the association rules extracted from your market basket data.  
Select a product and let the app automatically show the items that are often purchased together.
""")

# Load the association rules CSV generated earlier
rules_file = "/Users/zen/Documents/Datasets for ML/association_rules.csv"
try:
    rules = pd.read_csv(rules_file)
    if rules.empty:
        st.error("The association rules file is empty. Please check your data or model parameters.")
        st.stop()
    else:
        st.success("Association rules loaded successfully!")
except Exception as e:
    st.error(f"Error loading association rules: {e}")
    st.stop()

# Ensure that the 'antecedents' column is in frozenset format
if 'antecedents' not in rules.columns:
    st.error("The rules dataset does not contain an 'antecedents' column.")
    st.stop()

# Clean up the antecedents column: convert string representations to frozensets if needed
rules['antecedents'] = rules['antecedents'].apply(parse_antecedent)
rules['consequents'] = rules['consequents'].apply(parse_antecedent)

# Extract unique items from the antecedents
unique_items = set()
for antecedent in rules['antecedents']:
    unique_items.update(antecedent)
unique_items = sorted(unique_items)

# Create a selectbox for the user to choose an item
selected_item = st.selectbox("Select a product to get recommendations:", unique_items)

# Filter the rules to those where the selected item is in the antecedents
filtered_rules = rules[rules['antecedents'].apply(lambda x: selected_item in x)]

st.subheader("Predicted Associated Items")
if filtered_rules.empty:
    st.info(f"No association rules found for **{selected_item}**. Try selecting a different product!")
else:
    # Sort the filtered rules by lift in descending order
    filtered_rules = filtered_rules.sort_values(by="lift", ascending=False)
    
    # Extract unique recommended items from the consequents
    recommended_items = set()
    for consequent in filtered_rules["consequents"]:
        recommended_items.update(consequent)
    
    # Remove the selected item from recommendations if it appears
    recommended_items.discard(selected_item)
    
    if recommended_items:
        st.write(f"Customers who purchase **{selected_item}** also tend to purchase:")
        st.markdown(", ".join(f"**{item}**" for item in recommended_items))
    else:
        st.info("No additional recommendations available.")

st.markdown("---")
st.markdown("### Keep exploring and have fun discovering hidden patterns in your data! 🎈")
