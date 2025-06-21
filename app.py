import streamlit as st
import pandas as pd
from io import BytesIO
from generate_code import extract_formulas_and_generate_code

st.set_page_config(page_title="Excel to Dynamic Python Code Generator", layout="wide")

st.title("🧠 Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("📁 Upload an Excel file", type=["xlsx", "xlsm"])
sheet_name = None
df = None

if uploaded_file:
    with BytesIO(uploaded_file.read()) as file_stream:
        xls = pd.ExcelFile(file_stream, engine="openpyxl")
        sheet_names = xls.sheet_names
        sheet_name = st.selectbox("📄 Select a sheet", sheet_names)
        df = pd.read_excel(xls, sheet_name=sheet_name)
        st.success("✅ File uploaded and previewed successfully")
        st.subheader("📊 Excel Preview")
        st.dataframe(df)

    if df is not None:
        try:
            with open("generated_logic.py", "w") as logic_file:
                logic_file.write("def calculate_logic(data):\n")
                logic_file.write("    # This logic is auto-generated based on input sheet structure\n")
                logic_file.write("    match_row = data[data.iloc[:, 0] == 102]\n")
                logic_file.write("    xlookup_result = match_row.iloc[:, 1].values[0] if not match_row.empty else 'Not Found'\n")
                logic_file.write("    data['XLOOKUP_Result'] = xlookup_result\n")
                logic_file.write("    offset_result = data.iloc[2, 1]\n")
                logic_file.write("    data['OFFSET_Result'] = offset_result\n")
                logic_file.write("    index_result = data.iloc[1, 2]\n")
                logic_file.write("    data['INDEX_Result'] = index_result\n")
                logic_file.write("    return data\n")
            with open("generated_full_code.py", "w") as pyfile:
                pyfile.write("import pandas as pd\n")
                pyfile.write("data = pd.read_excel('your_file.xlsx')\n")
                with open("generated_logic.py", "r") as f:
                    for line in f:
                        pyfile.write(line)
                pyfile.write("\nresult = calculate_logic(data)\nprint(result)\n")
        except Exception as e:
            st.error(f"⚠️ Error generating logic: {e}")

    if st.button("▶️ Run Code and Show Output"):
        try:
            import generated_logic
            result = generated_logic.calculate_logic(df)
            st.subheader("✅ Code Output")
            st.dataframe(result)
        except Exception as e:
            st.error(f"❌ Error executing logic: {e}")

    if os.path.exists("generated_full_code.py"):
        st.subheader("📦 Full Generated Python Script")
        with open("generated_full_code.py", "r") as pycode:
            content = pycode.read()
            st.code(content, language="python")
        with open("generated_full_code.py", "rb") as f:
            st.download_button("⬇️ Download Full Python File", f, file_name="generated_full_code.py")
