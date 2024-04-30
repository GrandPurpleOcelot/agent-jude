import io
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

# Set the page title
st.set_page_config(page_title="PDF Viewer")

# Add a file uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# If a file is uploaded, display it using the pdf_viewer
if uploaded_file is not None:
    with st.spinner("Loading PDF..."):
        # Convert the uploaded file to bytes
        file_bytes = uploaded_file.getvalue()
        pdf_viewer(file_bytes, height=800)