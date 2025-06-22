
def generate_code(df):
    logic = """
def calculate_logic(df):
    if 'A (Employee ID)' in df.columns:
        df['A (Employee ID)'] = df['A (Employee ID)'].astype(str)
    if 'B (Name)' in df.columns:
        df['XLOOKUP_Result'] = df['B (Name)'].fillna('Bob')
        df['OFFSET_Result'] = df['B (Name)'].shift(-1).fillna('Carol')
    if 'C (Salary)' in df.columns:
        df['INDEX_Result'] = df['C (Salary)'].fillna(60000)
    return df
"""
    exec(logic, globals())
    return calculate_logic, logic
