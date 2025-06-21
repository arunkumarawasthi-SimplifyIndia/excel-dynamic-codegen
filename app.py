import streamlit as st
import pandas as pd
import os
from generate_code import generate_python_logic
from generated_full_code import calculate_logic

st.set_page_config(layout="wide")

st.image("https://i.imgur.com/LNw9nHO.png", width=120)
st.title("Excel to Dynamic Python Code Generator")
st.subheader("🧠 Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    file_path = f"temp_uploaded/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names

    selected_sheet = st.selectbox("Select Worksheet", sheet_names)
    df = pd.read_excel(file_path, sheet_name=selected_sheet)

    st.success("✅ File uploaded and previewed successfully")
    st.subheader("📊 Excel Preview")
    st.dataframe(df)

    st.subheader("🛠️ Generated Python Code")
    generated_code = generate_python_logic(df)
    st.code(generated_code, language="python")

    full_code = f"""import pandas as pd

data = pd.read_csv('temp_data.csv')

{generated_code}

result = calculate_logic(data)
print(result)
""" 

    with open("generated_full_code.py", "w") as f:
        f.write(full_code)

    st.subheader("📦 Full Generated Python Script")
    st.code(full_code, language="python")

    st.download_button("⬇️ Download Full Python File", file_name="generated_code.py", mime="text/x-python", data=full_code)

    if st.button("▶️ Run Code and Show Output"):
        try:
            df.to_csv("temp_data.csv", index=False)
            import generated_full_code as temp_module
            result_df = temp_module.calculate_logic(df)
            st.dataframe(result_df)
        except Exception as e:
            st.error(f"❌ Error executing logic: {e}")
