import streamlit as st
from docx import Document
from io import BytesIO
import os
from docx2pdf import convert
import base64

def load_docx(document):
    doc = Document(document)
    return doc

def modify_docx(doc, new_text):
    for para in doc.paragraphs:
        if '[targeted_text]' in para.text:
            para.text = new_text
    return doc

def save_docx(doc):
    buffer = BytesIO()
    doc.save(buffer)
    return buffer

def docx_to_pdf(docx_path, pdf_path):
    # Convert DOCX to PDF using docx2pdf
    convert(docx_path, pdf_path)

def main():
    st.title('DOCX Editor App')

    # Ensure the temp directory exists
    temp_dir = "./temp"
    os.makedirs(temp_dir, exist_ok=True)

    uploaded_file = st.file_uploader("Choose a .docx file", type="docx")
    if uploaded_file is not None:
        document = load_docx(uploaded_file)

        user_input = st.text_input("New text to replace placeholders:", "Type here...")
        
        if st.button("Modify Document"):
            modified_doc = modify_docx(document, user_input)
            buffer = save_docx(modified_doc)
            buffer.seek(0)
            
            # Save the modified DOCX to a file in the temp directory
            temp_docx_path = os.path.join(temp_dir, 'modified_document.docx')
            with open(temp_docx_path, 'wb') as f:
                f.write(buffer.getvalue())
            
            # Create a PDF path in the temp directory
            pdf_path = os.path.join(temp_dir, 'temporary_copy.pdf')
            
            # Convert DOCX to PDF
            print("++++++++++++++++++", temp_docx_path, pdf_path)
            convert(temp_docx_path)
            
            # Display the PDF
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="Download modified DOCX",
                    data=buffer,
                    file_name="modified_document.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                st.write("Modified Document Preview:")
                st.components.v1.html(
                    f'<iframe src="data:application/pdf;base64,{base64.b64encode(pdf_bytes).decode()}" width="700" height="1000" type="application/pdf"></iframe>',
                    height=1000
                )

if __name__ == "__main__":
    main()