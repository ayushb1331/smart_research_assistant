import PyPDF2

def extract_text_from_file(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text
    else:
        return ""