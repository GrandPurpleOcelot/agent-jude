import streamlit as st
from docx import Document
from io import BytesIO
import os
from docx2pdf import convert
import base64
import mammoth
import openai

# Connect to OpenAI key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to load a DOCX file
def load_docx(document):
    """Loads a Microsoft Word document.
    
    Args:
        document (str or file-like object): The path to the Word document file or a file-like object containing the document.
    
    """Generates content for a document based on natural language instructions using OpenAI's GPT-4 model.
    
    Args:
        doc (Document): The document object to be modified.
        nl_instruction (str): Natural language instruction for content generation.
    
    Returns:
        Document: The modified document with generated content inserted.
    """
    Returns:
        Document: A python-docx Document object representing the loaded Word document.
    """
    doc = Document(document)
    return doc

# Function to generate content using OpenAI and replace targeted text
def generate_content(doc, nl_instruction):
    instruction_message = f"You are a professional business analyst. Your task is to generate a report based on the user's requirements. Do not use markdown format for your response."

    openai_response = openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": instruction_message},
            {"role": "user", "content": nl_instruction}
        ],
        temperature=0.5,
        stream=False,
    )
    generated_text = openai_response.choices[0].message.content
    
    for para in doc.paragraphs:
        if '[targeted_text]' in para.text:
            para.text = generated_text
    return doc

# Function to save a DOCX file to a buffer
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

# Function to convert DOCX to HTML
def docx_to_html(docx_path, html_path):
    """
    Converts a DOCX file to HTML format.
    
    Args:
        docx_path (str): The file path of the input DOCX file.
        html_path (str): The file path where the output HTML will be saved.
    
    Returns:
        bool: True if the conversion was successful, False otherwise.
    """
    try:
        with open(docx_path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            """
            Main function for the DOCX Editor App.
            
            This function sets up the Streamlit interface for a DOCX editing application. It allows users to upload a .docx file, 
            provide natural language instructions for content generation, and then generates and displays the modified document.
            
            Args:
                None
            
            Returns:
                None: This function doesn't return anything, but it updates the Streamlit UI.
            
            """
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

        nl_instruction = st.text_area("Describe your content requirements:", "Type your instructions here...")
        
        if st.button("Generate documentation",use_container_width=True):
            modified_doc = generate_content(document, nl_instruction)
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
                    st.markdown(html_content, unsafe_allow_html=True)
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