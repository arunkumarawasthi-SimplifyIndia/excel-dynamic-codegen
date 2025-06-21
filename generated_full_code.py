
def calculate_logic(data):
    try:
        match_row = data[data['A (Employee ID)'] == 102]
        xlookup_result = match_row['B (Name)'].values[0] if not match_row.empty else 'Not Found'
        data['XLOOKUP_Result'] = xlookup_result

        offset_result = data.iloc[2, 1]  # 3rd row, 2nd column (Name: Carol)
        data['OFFSET_Result'] = offset_result

        index_result = data['C (Salary)'].iloc[1]  # Row 2 of Salary, which is 60000 for Bob
        data['INDEX_Result'] = index_result

    except Exception as e:
        raise e
    return data
