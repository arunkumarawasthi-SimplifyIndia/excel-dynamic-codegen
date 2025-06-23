
def calculate(data, computation_sheet):
    data['D2_processed'] = computation_sheet.iloc[:, 1].iloc[0]  # from VLOOKUP
    data['F2_processed'] = computation_sheet.iloc[:, 4].iloc[0]  # from VLOOKUP
    data['D3_processed'] = computation_sheet.iloc[:, 6].iloc[0]  # from VLOOKUP
    data['D4_processed'] = computation_sheet.iloc[:, 47].iloc[0]  # from VLOOKUP
    data['F4_processed'] = computation_sheet.iloc[:, 6].iloc[0]  # from VLOOKUP
    data['D5_processed'] = computation_sheet.iloc[:, 8].iloc[0]  # from VLOOKUP
    data['B8_processed'] = computation_sheet.iloc[:, 20].iloc[0]  # from VLOOKUP
    data['D8_processed'] = computation_sheet.iloc[:, 20].iloc[0]  # from VLOOKUP
    data['F8_processed'] = data['D8'].astype(float) - data['B8'].astype(float)
    data['B10_processed'] = computation_sheet.iloc[:, 20].iloc[0]  # from VLOOKUP
    data['B12_processed'] = computation_sheet.iloc[:, 24].iloc[0]  # from VLOOKUP
    data['D12_processed'] = computation_sheet.iloc[:, 28].iloc[0]  # from VLOOKUP
    data['B18_processed'] = 'NumToWords logic to be implemented'
    return data
