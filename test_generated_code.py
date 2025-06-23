import pandas as pd
from generated_logic import calculate

# Load your original Excel file
df = pd.read_excel("your_excel_file.xlsx")

# Call the generated function
result_df = calculate(df)

# Display output
print("\n🔍 Processed Data:")
print(result_df.head())  # Show first 5 rows
