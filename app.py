import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tabular File Matcher", layout="wide")
st.title("📋 Tabular File Matcher")
st.write("Paste your 3-column table and upload files to verify matches.")

# Create two main columns for input
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Upload Files")
    uploaded_files = st.file_uploader("Drop files here", accept_multiple_files=True)
    uploaded_names = [f.name for f in uploaded_files] if uploaded_files else []
    
    if uploaded_names:
        st.success(f"{len(uploaded_names)} files uploaded.")

with col2:
    st.subheader("2. Paste Table Data")
    st.info("Paste your 3 columns below (Ctrl+V). Tip: Ensure your 'File Name' column is included.")
    
    # Initialize an empty dataframe with 3 columns if not already there
    default_df = pd.DataFrame([["", "", ""]] * 5, columns=["Column 1", "Column 2", "File Name"])
    
    # Data editor allows direct pasting from Excel/Sheets
    pasted_df = st.data_editor(
        default_df, 
        num_rows="dynamic", 
        use_container_width=True,
        hide_index=True
    )

st.divider()

# Logic to handle the comparison
if uploaded_names and not pasted_df.empty:
    st.subheader("3. Comparison Results")
    
    # Select which column contains the filenames
    target_col = st.selectbox("Which column contains the File Names?", options=pasted_df.columns, index=2)
    
    # Clean the pasted names (remove empty rows and whitespace)
    expected_names = pasted_df[target_col].dropna().apply(lambda x: str(x).strip()).tolist()
    expected_names = [name for name in expected_names if name != ""]

    set_uploaded = set(uploaded_names)
    set_expected = set(expected_names)

    # 1. Missing Files (In Table but not Uploaded)
    missing = set_expected - set_uploaded
    # 2. Extra Files (Uploaded but not in Table)
    extra = set_uploaded - set_expected

    res_col1, res_col2 = st.columns(2)

    with res_col1:
        if missing:
            st.error(f"❌ Missing Files ({len(missing)})")
            for m in missing:
                st.write(f"⁃ `{m}`")
        else:
            st.success("✅ No missing files!")

    with res_col2:
        if extra:
            st.warning(f"➕ Extra Files ({len(extra)})")
            for e in extra:
                st.write(f"⁃ `{e}`")
        else:
            st.info("ℹ️ No extra files found.")

    if not missing and not extra and len(expected_names) > 0:
        st.balloons()
        st.success("Perfect Match! All items in the table are present in the upload.")

else:
    st.warning("Waiting for both file uploads and pasted table data...")
