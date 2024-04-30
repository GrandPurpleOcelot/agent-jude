import os
from pylatex import Document, Command
from pylatex.utils import NoEscape
import subprocess
import os

def compile_tex_to_pdf(tex_filename):
    # Check if the .tex file exists
    if not os.path.exists(tex_filename):
        print(f"Error: The file {tex_filename} does not exist.")
        return

    # Compile the .tex file using pdflatex
    command = ['pdflatex', '-interaction=nonstopmode', tex_filename]
    try:
        subprocess.run(command, check=True)
        print(f"PDF has been successfully created from {tex_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to compile {tex_filename}. Error: {e}")

if __name__ == "__main__":
    compile_tex_to_pdf("sample.tex")