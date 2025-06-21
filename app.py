
import streamlit as st
import pandas as pd
from io import BytesIO
from generate_code import generate_python_logic
from generated_logic import calculate_logic

st.set_page_config(page_title="Excel to Dynamic Python Code Generator", layout="wide")

st.markdown("## 🧠 Excel to Dynamic Python Code Generator")
uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx", "xlsm"])

if uploaded_file:
    st.success("✅ File uploaded and previewed successfully")
    data = pd.read_excel(uploaded_file)
    st.subheader("📊 Excel Preview")
    st.dataframe(data)

    try:
        generated_code = generate_python_logic(data)
        st.subheader("🛠️ Generated Python Code")
        st.code(generated_code, language="python")

        st.subheader("📦 Full Generated Python Script")
        full_code = f"""import pandas as pd\n\ndata = pd.read_excel('your_file.xlsx')\n\n{generated_code}\n\nresult = calculate_logic(data)\nprint(result)\n"""
        st.code(full_code, language="python")

        if st.button("▶️ Run Code and Show Output"):
            result_df = calculate_logic(data)
            st.success("✅ Code executed successfully. Here's the result:")
            st.dataframe(result_df)

    except Exception as e:
        st.error(f"❌ Error executing logic: {str(e)}")
