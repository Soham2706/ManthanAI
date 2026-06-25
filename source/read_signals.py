from docx import Document

doc = Document(
    "../data/redrob_signals_doc.docx"
)

for para in doc.paragraphs:
    print(para.text)