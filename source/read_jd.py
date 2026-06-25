from docx import Document

doc = Document(
    "../data/job_description.docx"
)

text = []

for p in doc.paragraphs:
    text.append(p.text)

jd = "\n".join(text)

with open(
    "../outputs/jd.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(jd)

print(jd[:1000])