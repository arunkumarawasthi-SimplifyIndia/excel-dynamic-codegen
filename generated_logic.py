def calculate_logic(data):
    # This logic is auto-generated based on input sheet structure
    match_row = data[data.iloc[:, 0] == 102]
    xlookup_result = match_row.iloc[:, 1].values[0] if not match_row.empty else 'Not Found'
    data['XLOOKUP_Result'] = xlookup_result
    offset_result = data.iloc[2, 1]
    data['OFFSET_Result'] = offset_result
    index_result = data.iloc[1, 2]
    data['INDEX_Result'] = index_result
    return data
