import pandas as pd

def generate_full_python_code(df):
    def calculate(data):
        match_row = data[data['A'] == 102]
        xlookup_result = match_row['B'].values[0] if not match_row.empty else "Not Found"
        data['XLOOKUP_Result'] = xlookup_result

        offset_result = data.iloc[2, 1]  # Adjust column index if needed
        data['OFFSET_Result'] = offset_result

        index_result = data['C'].iloc[1]
        data['INDEX_Result'] = index_result

        return data

    result = calculate(df.copy())
    return result
