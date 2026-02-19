import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart File Matcher", layout="wide")

# --- Reset Logic ---
def reset_app():
    st.session_state["file_uploader_key"] += 1
    st.session_state["data_editor_key"] += 1

if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0
if "data_editor_key" not in st.session_state:
    st.session_state["data_editor_key"] = 100

# --- Header ---
top_col1, top_col2 = st.columns([5, 1])
with top_col1:
    st.title("📁 Smart File Matcher")
with top_col2:
    st.write(" ") 
    if st.button("🔄 Reset All", use_container_width=True, on_click=reset_app):
        st.rerun()

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
    st.subheader("2. Paste Expected Names")
    init_df = pd.DataFrame([["", "", ""]] * 10, columns=["Col 1", "Col 2", "Col 3"])
    pasted_df = st.data_editor(
        init_df, 
        num_rows="dynamic", 
        use_container_width=True,
        hide_index=True,
        key=f"editor_{st.session_state['data_editor_key']}"
    )

st.divider()

# --- Match Logic ---
has_uploaded = len(uploaded_names) > 0
has_pasted = not pasted_df.replace('', pd.NA).dropna(how='all').empty

if has_uploaded or has_pasted:
    # Clean pasted data
    raw_pasted_names = pasted_df.values.flatten()
    expected_names = set([str(name).strip() for name in raw_pasted_names if str(name).strip()])

    # Direct Matches
    missing = expected_names - uploaded_names
    extra = uploaded_names - expected_names

    st.subheader("3. Match Analysis")

    # --- THE "REMAINING TO BE MATCHED" LOGIC ---
    # If there is exactly 1 missing and 1 extra, they are likely the same file
    if len(missing) == 1 and len(extra) == 1:
        st.warning("💡 **Potential Match Found!**")
        m_file = list(missing)[0]
        e_file = list(extra)[0]
        st.info(f"The file `{e_file}` you uploaded is likely intended to match `{m_file}` from your list, but the names don't match exactly.")
    
    elif len(missing) > 0 and len(extra) > 0:
        st.info(f"📝 You have {len(missing)} items left in your list and {len(extra)} extra files uploaded. Check for typos below.")

    # Standard Results Display
    res_a, res_b = st.columns(2)
    
    with res_a:
        if missing:
            st.error(f"❌ Missing from Uploads ({len(missing)})")
            for m in sorted(missing):
                st.write(f"• `{m}`")
        else:
            st.success("✅ All listed names found!")

    with res_b:
        if extra:
            st.warning(f"➕ Unmatched Uploads ({len(extra)})")
            for e in sorted(extra):
                st.write(f"• `{e}`")
        else:
            st.success("✅ No extra files found!")

    if not missing and not extra and expected_names:
        st.balloons()
        st.success("🎉 Perfect 1:1 Match!")
else:
    st.info("Upload files and paste your table to begin.")
