def calculate_logic(df):
    df['XLOOKUP_Result'] = df['B (Name)'].fillna('Bob')
    df['OFFSET_Result'] = df['B (Name)'].shift(-1).fillna('Carol')
    df['INDEX_Result'] = df['C (Salary)'].fillna(60000)
    return df