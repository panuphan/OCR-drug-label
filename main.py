from OCR import tesseract
# tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract'

img_path='env\\images\\1.png'
# custom_config = r'-l eng+tha -c preserve_interword_spaces=1'

text=tesseract(img_path)
print(text)
