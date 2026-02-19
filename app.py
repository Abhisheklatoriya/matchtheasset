import streamlit as st
import pandas as pd

st.set_page_config(page_title="4-Column File Matcher", layout="wide")

# --- Reset Logic ---
def reset_app():
    st.session_state["file_uploader_key"] += 1
    st.session_state["data_editor_key"] += 1

if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0
if "data_editor_key" not in st.session_state:
    st.session_state["data_editor_key"] = 100

# --- Top Header & Reset Button ---
top_col1, top_col2 = st.columns([5, 1])
with top_col1:
    st.title("📁 4-Column File Matcher")
with top_col2:
    st.write(" ") 
    if st.button("🔄 Reset All", use_container_width=True, on_click=reset_app):
        st.rerun()

st.write("Paste your 4 columns of filenames below and upload your files to verify they match.")

# --- UI Layout ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Upload Files")
    uploaded_files = st.file_uploader(
        "Upload files here", 
        accept_multiple_files=True,
        key=f"uploader_{st.session_state['file_uploader_key']}"
    )
    uploaded_names = set([f.name for f in uploaded_files]) if uploaded_files else set()
    
    if uploaded_names:
        st.success(f"✅ {len(uploaded_names)} files uploaded.")

with col2:
    st.subheader("2. Paste Expected Names (4 Columns)")
    st.info("Paste your Excel/Table data below. All 4 columns will be checked.")
    
    # Updated to 4 columns: Col A, B, C, and D
    init_df = pd.DataFrame([["", "", "", ""]] * 10, columns=["Col A", "Col B", "Col C", "Col D"])
    
    pasted_df = st.data_editor(
        init_df, 
        num_rows="dynamic", 
        use_container_width=True,
        hide_index=True,
        key=f"editor_{st.session_state['data_editor_key']}"
    )

st.divider()

# --- Process the comparison ---
has_uploaded = len(uploaded_names) > 0
has_pasted = not pasted_df.replace('', pd.NA).dropna(how='all').empty

if not has_uploaded and not has_pasted:
    st.info("Waiting for file uploads and pasted data...")
else:
    # Flatten all 4 columns into a single list
    raw_pasted_names = pasted_df.values.flatten()
    expected_names = set([str(name).strip() for name in raw_pasted_names if str(name).strip()])

    st.subheader("3. Match Analysis")
    
    missing = expected_names - uploaded_names
    extra = uploaded_names - expected_names

    if not missing and expected_names:
        st.success("✨ All pasted filenames were found in the uploaded batch!")
        if not extra:
            st.balloons()
    
    res_a, res_b = st.columns(2)
    
    with res_a:
        if missing:
            st.error(f"❌ Missing Files ({len(missing)})")
            for m in sorted(missing):
                st.write(f"• `{m}`")
        elif has_pasted:
            st.success("✅ All listed files are present.")

    with res_b:
        if extra:
            st.warning(f"➕ Extra Files ({len(extra)})")
            for e in sorted(extra):
                st.write(f"• `{e}`")
