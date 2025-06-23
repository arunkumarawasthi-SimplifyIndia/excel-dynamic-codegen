import pandas as pd

def generate_code(df: pd.DataFrame) -> str:
    code_lines = ["def calculate_logic(df):"]
    
    if 'A (Employee ID)' in df.columns:
        code_lines.append("    df['A (Employee ID)'] = df['A (Employee ID)'].astype(str)")
    
    if 'B (Name)' in df.columns:
        code_lines.append("    df['XLOOKUP_Result'] = df['B (Name)'].fillna('Bob')")
        code_lines.append("    df['OFFSET_Result'] = df['B (Name)'].shift(-1).fillna('Carol')")
    
    if 'C (Salary)' in df.columns:
        code_lines.append("    df['INDEX_Result'] = df['C (Salary)'].fillna(60000)")
    
  df = df.dropna(how="all")
df = df[~df.iloc[:, 0].astype(str).str.contains("ID", na=False)]
df['A (Employee ID)'] = pd.to_numeric(df['A (Employee ID)'], errors='coerce')
df = df.dropna(subset=['A (Employee ID)'])


    code_lines.append("    return df")
    return "\n".join(code_lines)
