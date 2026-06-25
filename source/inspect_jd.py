from docx import Document

doc = Document("../data/job_description.docx")

full_text = []

for para in doc.paragraphs:
    full_text.append(para.text)

jd = "\n".join(full_text)

print(jd)