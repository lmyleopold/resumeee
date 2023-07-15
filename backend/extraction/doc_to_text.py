import os
import fitz
import base64
import docx2pdf
from PIL import Image
from operator import itemgetter
from ecloud import CMSSEcloudOcrClient


temp = "temp.pdf"
temp_image = "temp.png"
accesskey = '0192cccf8c8a419481f09825e7bd0266'
secretkey = 'ae178f4b1b76417c8e0e47aeed27d294'
url = 'https://api-wuxi-1.cmecloud.cn:8443'

def request_generic_base64(imagepath):
    requesturl = '/api/ocr/v1/generic'
    with open(imagepath, 'rb') as f:
        img = f.read()
        image_base64 = base64.b64encode(img).decode('utf-8')
        ocr_client = CMSSEcloudOcrClient(accesskey, secretkey, url)
        response = ocr_client.request_ocr_service_base64(requestpath=requesturl,base64=image_base64)
        return eval(response.text)
        # print(eval(response.text))

def dict_to_text(dict):
    prism_wordsInfo = dict['body']['content']['prism_wordsInfo']
    texts = []
    for data in prism_wordsInfo:
        text = data['word']
        x = data['position'][0]['x']
        y = data['position'][0]['y']
        texts.append({"text": text, "x": x, "y": y})
    return texts

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

    if len(output) <= 100: # maybe ocr file?
        page_texts = []
        for page in pdf:
            rect = page.rect  # 获取页面大小
            mat = fitz.Matrix(2, 2)  # 设置缩放因子，可根据需要调整
            pix = page.get_pixmap(matrix=mat, alpha=False)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            image.save("temp.png")
            data = request_generic_base64("temp.png")
            texts = dict_to_text(data)
            page_texts.extend(texts)
        output = "".join(text["text"] for text in page_texts)

    pdf.close()
    return output