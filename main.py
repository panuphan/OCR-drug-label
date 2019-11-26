import cv2
import numpy as np
from OCR import tesseract
from skew_correction.skewer import Skewer

# tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract'
img_path='env\\images\\1.png'
# custom_config = r'-l eng+tha -c preserve_interword_spaces=1'

def preprocessing():
    img=cv2.imread(img_path)
    imgcp=img.copy()
    # img_resize=cv2.resize(imgcp,None,fx=1.5,fy=1.5)
    img_gray= cv2.cvtColor(imgcp,cv2.COLOR_BGR2GRAY)
    cv2.imwrite("img_gray.png",img_gray)

    # kernel=np.ones((3,3),np.uint8)
    # dilate=cv2.dilate(img_gray,kernel,iterations=1)
    # erosion=cv2.erode(dilate,kernel,iterations=1)
    # cv2.imwrite("erosion.png",erosion)


    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    im = cv2.filter2D(img_gray, -1, kernel)
    cv2.imwrite("filter2D.png",im)

    # img_thd=cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    # cv2.imwrite("adaptiveThreshold.png",img_thd)

def skewCorrection(img_path):
    img=cv2.imread(img_path)
    img=img.copy()
    # img_resize=cv2.resize(imgcp,None,fx=0.5,fy=0.5)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # edged = cv2.Canny(gray, 10, 50)

    skewer = Skewer(image_data=img)
    rotated = skewer.get_rotated()

    if skewer.is_rotated(): # Returns true or false according to any skew operation
        cv2.imshow("Rotated image", rotated)
        cv2.imshow("image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
def correct_skew(img_path,verbose=False):
    image = cv2.imread(img_path)
    image = cv2.resize(image,None,fx=1.5,fy=1.5)
    image=image.copy()
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45: angle = -(90 + angle)
    else: angle = -angle
    
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
	    flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    # cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
	# (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    if verbose:
        print("[INFO] angle: {:.3f}".format(angle))
        cv2.imshow("Input", image)
        cv2.imshow("Rotated", rotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return rotated

img =correct_skew(img_path,verbose=True)

text=tesseract(img)
print(text)

# json={"name":"","hn":"006431-59","dose":"","instruction":"ORAL 1 TSP,PRN","itemId":"",
# "med_name":"Paracet syr 120 mg/5ml","date":"23/08/2562","hospital_number":"11305",
# "amount":"1.00","usage":"","remark":""
# }