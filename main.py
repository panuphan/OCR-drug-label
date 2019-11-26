import cv2
import numpy as np
import pytesseract
from imutils.perspective import four_point_transform
import imutils

# tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract'
img_path='env\\images\\skew\\6.jpg'
# img_path='env\\images\\1.png'
# custom_config = r'-l eng+tha -c preserve_interword_spaces=1'

def imshow(*args,**kwargs):
    """ 
    example:
        imshow("title",image)
        imshow(image)
        imshow("title",image=image)
        imshow(title="title",image=image)
        imshow([("title1",image1),image2])

    """
    
    if kwargs.get("title") and kwargs.get("image"):
        cv2.imshow(kwargs.get("title") ,kwargs.get("image"))
    elif kwargs.get("image"):
        title = args[0] if args[0] else "-"
        cv2.imshow(title,kwargs.get("image"))
    if len(args)==1:
        if isinstance(args[0],list): 
            for p in args[0]:
                if isinstance(p,tuple): 
                    title,image=p
                elif isinstance(p,np.ndarray):
                    title,image="",p
                cv2.imshow(title,image)
        
        elif isinstance(args[0],np.ndarray):
            cv2.imshow("",args[0])
    elif len(args)==2:
        title,image=args
        cv2.imshow(title,image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def tesseract(image_path,config=r'--oem 1 -l eng+tha -c preserve_interword_spaces=1',tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract'):
    pytesseract.pytesseract.tesseract_cmd=tesseract_path
    return pytesseract.image_to_string(image_path, config=config)

def correct_skew(image,verbose=False):
    # image = cv2.resize(image,None,fx=0.5,fy=0.5)
    orig=image.copy()
    
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
        imshow([("Input", image),("Rotated", rotated)])
    
    return rotated

def perspective_transform(image,verbose=False):
    orig = image.copy()
    ratio = orig.shape[0] / 500.0
    image = imutils.resize(image, height = 500)
    
  ############# STEP 1: Edge Detection ######################

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    
    if verbose:
        # show the original image and the edge detected image
        print("STEP 1: Edge Detection")
        imshow([("Image", image),("Edged", edged)])

  ############# STEP 2: Find contours of paper ######################

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    
        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break
    
    if verbose:
        # show the contour (outline) of the piece of paper
        print("STEP 2: Find contours of paper")
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
        imshow([("Outline", image)])

  ############## STEP 3: Perspective transform #####################

    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    if verbose:
        # show the original and scanned images
        print("STEP 3: Apply perspective transform")
        imshow([
            ("Original", imutils.resize(orig, height = 650)),
            ("Scanned", imutils.resize(warped, height = 650))])
    
    return imutils.resize(warped, height = 650)

img_path='env\\images\\1.png'
img=cv2.imread(img_path)
# img = correct_skew(img,True)
img = perspective_transform(img)
text=tesseract(img)
print(text)
imshow(img)


# json={"name":"","hn":"006431-59","dose":"","instruction":"ORAL 1 TSP,PRN","itemId":"",
# "med_name":"Paracet syr 120 mg/5ml","date":"23/08/2562","hospital_number":"11305",
# "amount":"1.00","usage":"","remark":""
# }

