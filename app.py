
import streamlit as st
import pandas as pd

st.set_page_config(page_title="OD Data Verifier", layout="wide")

st.title("📝 OD Data Verification Form")

# Upload Excel file
uploaded_file = st.file_uploader("Upload your OD Report Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    if 'Verified Name' not in df.columns:
        df['Verified Name'] = ""
    if 'Match Status' not in df.columns:
        df['Match Status'] = ""

    index = st.number_input("Record Number", min_value=0, max_value=len(df)-1, step=1)
    row = df.loc[index]

    st.markdown(f"### Original Name: `{row['Party Name']}`")
    st.text(f"Father/Spouse Name: {row['Father / Spouse Name']}")
    st.text(f"Phone: {row['Customer Phone NO']}")
    st.text(f"Address: {row['Customer Address']}")

    entered_name = st.text_input("Enter Verified Name", value=row['Verified Name'])
    df.at[index, 'Verified Name'] = entered_name

    # Simple matching logic
    match_suggestion = "Matched" if str(row['Party Name']).lower() in str(entered_name).lower() else "Not Matched"

    match_status = st.radio("Match Status", options=["Matched", "Not Matched", "Auto"], index=2)

    final_status = match_suggestion if match_status == "Auto" else match_status
    df.at[index, 'Match Status'] = final_status

    st.success(f"✅ Final Match Status: {final_status}")

    # Download option
    if st.button("💾 Download Updated Excel"):
        df.to_excel("verified_od_data.xlsx", index=False)
        with open("verified_od_data.xlsx", "rb") as f:
            st.download_button("Click to Download", f, file_name="verified_od_data.xlsx")
