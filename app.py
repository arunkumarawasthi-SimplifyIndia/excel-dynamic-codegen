
import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("📊 Excel to Dynamic Python Code Generator")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xlsm"])
if uploaded_file:
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet = st.selectbox("Select Sheet", xls.sheet_names)
        df = xls.parse(sheet)
        st.success("File uploaded and previewed successfully")
        st.subheader("📈 Excel Preview")
        st.dataframe(df)

        if st.button("▶️ Run Code and Show Output"):
            try:
                # Simple simulated logic: XLOOKUP, OFFSET, INDEX examples
                match_row = df[df[df.columns[0]] == 102]
                xlookup_result = match_row[df.columns[1]].values[0] if not match_row.empty else "Not Found"
                offset_result = df.iloc[2, 1] if len(df) > 2 else None
                index_result = df[df.columns[2]].iloc[1] if len(df) > 1 else None

                df["XLOOKUP_Result"] = xlookup_result
                df["OFFSET_Result"] = offset_result
                df["INDEX_Result"] = index_result

                st.success("Code executed successfully.")
                st.subheader("📋 Output Data")
                st.dataframe(df)

                # Display generated Python code
                generated_code = f"""import pandas as pd\n\ndf = pd.read_excel("your_file.xlsx")\nmatch_row = df[df['{df.columns[0]}'] == 102]\nxlookup_result = match_row['{df.columns[1]}'].values[0] if not match_row.empty else "Not Found"\noffset_result = df.iloc[2, 1] if len(df) > 2 else None\nindex_result = df['{df.columns[2]}'].iloc[1] if len(df) > 1 else None\n\ndf["XLOOKUP_Result"] = xlookup_result\ndf["OFFSET_Result"] = offset_result\ndf["INDEX_Result"] = index_result\nprint(df)"""
                st.subheader("🧠 Full Generated Python Script")
                st.code(generated_code, language="python")

            except Exception as e:
                st.error(f"Error executing logic: {e}")
    except Exception as e:
        st.error(f"Error reading file: {e}")
