import mammoth

with open("demo.docx", "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value

with open("demo.html", "w", encoding="utf-8") as html_file:
    html_file.write(html)