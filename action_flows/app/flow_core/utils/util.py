import pymupdf
import base64
import httpx

def read_pdf_text(file_path):
    doc = pymupdf.open(file_path) 
    content = ''
    for page in doc:
        text = page.get_text()
        content =  content + text
    return content


def read_image_from_url(image_url):
    return base64.b64encode(httpx.get(image_url).content).decode("utf-8")



def read_file(file_path):
    content = ''
    with open(file_path, 'r', encoding='Latin-1') as f:
        content = f.read()
    return content
