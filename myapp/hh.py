import PyPDF2
with open("C:/Users/DELL/Downloads/A%20reference%20book%20of%20computer%20graphics%20_250122_122601.pdf", "rb") as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    print(text)
