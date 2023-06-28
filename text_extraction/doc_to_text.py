import fitz
import docx2pdf
from operator import itemgetter
import os

temp = "text_extraction/temp.pdf"

def extract_text_with_position(page):
    text_instances = page.get_text("dict", flags=11)["blocks"]
    texts = []
    for inst in text_instances:
        for line in inst["lines"]:
            for span in line["spans"]:
                text = span["text"]
                bbox = span["bbox"]
                x0, y0, x1, y1 = bbox
                texts.append({"text": text, "x": x0, "y": y0})
    return texts

def doc_to_text(path, ext):
    if ext == ".docx":
        docx2pdf.convert(path, os.path.join(os.getcwd(), temp))
        pdf = fitz.open(temp)
    else:
        pdf = fitz.open(path)

    page_texts = []
    sorted_texts = []
    for page in pdf:
        texts = extract_text_with_position(page)
        page_texts.extend(texts)
        sorted_texts.extend(sorted(page_texts, key=itemgetter("y", "x")))
        page_texts.clear()
    
    output = "".join(text["text"] for text in sorted_texts)
    pdf.close()
    return output