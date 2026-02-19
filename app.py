import streamlit as st
import pandas as pd

st.set_page_config(page_title="Multi-Column File Matcher", layout="wide")

st.title("📁 Multi-Column File Matcher")
st.write("Paste your 3 columns of filenames below and upload your files to verify they match.")

# Create the UI layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Upload Files")
    uploaded_files = st.file_uploader("Upload files here", accept_multiple_files=True)
    # Store names of files actually uploaded
    uploaded_names = set([f.name for f in uploaded_files]) if uploaded_files else set()
    
    if uploaded_names:
        st.success(f"✅ {len(uploaded_names)} files uploaded.")

with col2:
    st.subheader("2. Paste Expected Names (3 Columns)")
    st.info("Paste your Excel/Table data below. All 3 columns will be checked.")
    
    # Initialize a table with 3 columns
    init_df = pd.DataFrame([["", "", ""]] * 10, columns=["Col A", "Col B", "Col C"])
    
    # The Data Editor allows pasting directly from Excel/Sheets
    pasted_df = st.data_editor(
        init_df, 
        num_rows="dynamic", 
        use_container_width=True,
        hide_index=True
    )

st.divider()

# Process the comparison
if not uploaded_names and pasted_df.values.flatten().tolist() == [""] * (len(pasted_df) * 3):
    st.info("Waiting for file uploads and pasted data...")
else:
    # 1. Flatten all 3 columns into a single list of names
    # 2. Convert to string, strip whitespace, and remove empty entries
    raw_pasted_names = pasted_df.values.flatten()
    expected_names = set([str(name).strip() for name in raw_pasted_names if str(name).strip()])

    st.subheader("3. Match Analysis")
    
    # Identify discrepancies
    missing = expected_names - uploaded_names
    extra = uploaded_names - expected_names

    if not missing and expected_names:
        st.success("✨ All pasted filenames were found in the uploaded batch!")
        if not extra:
            st.balloons()
    
    # Display Results in columns
    res_a, res_b = st.columns(2)
    
    with res_a:
        if missing:
            st.error(f"❌ Missing Files ({len(missing)})")
            st.caption("These names were in your table but NOT uploaded:")
            for m in sorted(missing):
                st.write(f"• `{m}`")
        else:
            st.write("✅ No missing files.")

    with res_b:
        if extra:
            st.warning(f"➕ Extra Files ({len(extra)})")
            st.caption("These files were uploaded but NOT in your table:")
            for e in sorted(extra):
                st.write(f"• `{e}`")
