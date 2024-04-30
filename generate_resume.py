import os
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape

def text_to_pdf(input_filename, output_filename):
    # Create a document
    doc = Document()
    
    # Read text from file
    with open(input_filename, 'r') as file:
        content = file.readlines()

    # Add content to the document
    with doc.create(Section('Text Content')):
        for line in content:
            doc.append(line)
    
    # Generate PDF
    doc.generate_pdf(output_filename, clean_tex=False)

if __name__ == "__main__":
    input_filename = 'sample.tex'
    output_filename = 'sample.pdf'
    text_to_pdf(input_filename, output_filename)