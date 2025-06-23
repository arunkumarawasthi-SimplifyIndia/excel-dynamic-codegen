import pandas as pd

def generate_code(df):
    # Auto-detect header row
    header_row = None
    for i in range(10):
        row = df.iloc[i]
        if row.notna().sum() >= 2:
            header_row = i
            break

    if header_row is None:
        raise ValueError("Could not detect header row.")

    df.columns = df.iloc[header_row]
    df = df[(header_row + 1):].reset_index(drop=True)
    df = df.dropna(how="all")

    # Sample logic generation (e.g., fill missing names or salaries)
    logic = []
    if "Name" in df.columns:
        df["XLOOKUP_Result"] = df["Name"].fillna("Bob")
        df["OFFSET_Result"] = df["Name"].shift(-1).fillna("Carol")
        logic.append("df['XLOOKUP_Result'] = df['Name'].fillna('Bob')")
        logic.append("df['OFFSET_Result'] = df['Name'].shift(-1).fillna('Carol')")

    if "Salary" in df.columns:
        df["INDEX_Result"] = df["Salary"].fillna(60000)
        logic.append("df['INDEX_Result'] = df['Salary'].fillna(60000)")

    generated_code = "\n".join(logic)
    return df, generated_code
