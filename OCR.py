import pytesseract
# custom_config = r'-l eng+tha -c preserve_interword_spaces=1'
# tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract'
# img_path='env\\images\\2.png'

def tesseract(image_path,config=r'--oem 1 -l eng+tha -c preserve_interword_spaces=1',tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract'):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    return pytesseract.image_to_string(image_path, config=config)

# text=tesseract(img_path)
# print(text)