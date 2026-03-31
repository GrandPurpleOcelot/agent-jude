import streamlit as st
from docx import Document
from io import BytesIO

def load_docx(document):
    """Loads a Microsoft Word document.
    
    Args:
        document (str or file-like object): The path to the .docx file or a file-like object containing the document.
    
    Returns:
        Document: A python-docx Document object representing the loaded Word document.
    """
    doc = Document(document)
    return doc

def modify_docx(doc, new_text):
    """Modifies a Word document by replacing a specific placeholder text with new text.
    
    Args:
        ```
        """Main function for the DOCX Editor App using Streamlit.
        
        This function sets up the user interface for uploading a .docx file,
        inputting replacement text, modifying the document, and downloading
        the modified version.
        
        Args:
            None
        
        Returns:
            None: This function doesn't return anything, it creates a Streamlit UI.
        """
        
        ```        doc (Document): The Word document object to be modified.
        new_text (str): The new text to replace the placeholder.
    
    Returns:
        Document: The modified Word document object.
    """
    for para in doc.paragraphs:
        if '[targeted_text]' in para.text:
            para.text = new_text
    return doc

def save_docx(doc):
    """Saves a docx document to a BytesIO buffer.
    
    Args:
        doc (Document): The docx document object to be saved.
    
    Returns:
        BytesIO: A buffer containing the saved document data.
    """
    buffer = BytesIO()
    doc.save(buffer)
    return buffer

def main():
    st.title('DOCX Editor App')

    uploaded_file = st.file_uploader("Choose a .docx file", type="docx")
    if uploaded_file is not None:
        document = load_docx(uploaded_file)
        print(document)
        user_input = st.text_input("New text to replace placeholders:", "Type here...")
        
        if st.button("Modify Document"):
            modified_doc = modify_docx(document, user_input)
            buffer = save_docx(modified_doc)
            buffer.seek(0)
            
            st.download_button(
                label="Download modified DOCX",
                data=buffer,
                file_name="modified_document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

if __name__ == "__main__":
    main()