import streamlit as st
from docx import Document
from io import BytesIO
import os
from docx2pdf import convert
import base64
import mammoth

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

def docx_to_html(docx_path, html_path):
    try:
        with open(docx_path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value

        with open(html_path, "w", encoding="utf-8") as html_file:
            html_file.write(html)
        return True
    except Exception as e:
        print(f"Failed to convert DOCX to HTML: {e}")
        return False

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
            
            # Create a HTML path in the temp directory
            html_path = os.path.join(temp_dir, 'temporary_copy.html')
            
            # Convert DOCX to HTML
            if docx_to_html(temp_docx_path, html_path):
                # Display the HTML if conversion was successful
                with open(html_path, "r", encoding="utf-8") as html_file:
                    html_content = html_file.read()
                    st.write("Modified Document Preview:")
                    st.html(html_content)
                    st.download_button(
                        label="Download modified DOCX",
                        data=buffer,
                        file_name="modified_document.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary"
                    )
            else:
                st.error("Failed to convert the document to HTML.")

if __name__ == "__main__":
    main()