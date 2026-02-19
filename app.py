import streamlit as st

# Set up the page title
st.set_page_config(page_title="File Matcher", page_icon="📁")
st.title("📁 File Matcher App")
st.write("Compare your uploaded files against a pasted list of expected file names.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Files")
    # Allow multiple file uploads
    uploaded_files = st.file_uploader("Upload your files here:", accept_multiple_files=True)
    
    # Extract the names of the uploaded files
    uploaded_filenames = []
    if uploaded_files:
        uploaded_filenames = [file.name for file in uploaded_files]
        st.write(f"**Total files uploaded:** {len(uploaded_filenames)}")

with col2:
    st.subheader("2. Paste Expected Names")
    # Text area for pasting filenames (one per line)
    pasted_text = st.text_area("Paste your list of file names (one per line):", height=150)
    
    # Clean up the pasted text into a list of strings
    expected_filenames = []
    if pasted_text:
        # Split by new line, remove empty spaces, and ignore blank lines
        expected_filenames = [name.strip() for name in pasted_text.split('\n') if name.strip()]
        st.write(f"**Total names pasted:** {len(expected_filenames)}")

st.divider()

# Only run the comparison if both inputs have data
if uploaded_filenames or expected_filenames:
    st.subheader("3. Match Results")
    
    # Convert lists to sets for easy mathematical comparison
    set_uploaded = set(uploaded_filenames)
    set_expected = set(expected_filenames)
    
    # Find the differences
    missing_files = set_expected - set_uploaded  # In expected, but not uploaded
    extra_files = set_uploaded - set_expected    # Uploaded, but not in expected
    
    # Check if they match perfectly
    if not missing_files and not extra_files:
        st.success("✅ Success! All uploaded files match the pasted list perfectly.")
        st.balloons()
    else:
        st.error("⚠️ There are discrepancies between your uploads and your list.")
        
        # Display missing files (what was pasted but not uploaded)
        if missing_files:
            st.warning("🔍 **Missing Files (Pasted, but not uploaded):**")
            for file in missing_files:
                st.write(f"- `{file}`")
                
        # Display extra files (what was uploaded but not pasted)
        if extra_files:
            st.info("➕ **Extra Files (Uploaded, but not in your pasted list):**")
            for file in extra_files:
                st.write(f"- `{file}`")
else:
    st.info("Upload files and paste your list to see the comparison results.")
