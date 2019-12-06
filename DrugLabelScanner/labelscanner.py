import cv2
import imutils
import pytesseract
from imutils.perspective import four_point_transform
import matplotlib.pyplot as plt
from skimage.morphology import dilation, erosion, closing, square
import pyzbar.pyzbar as pyzbar

def readDrugLabel(labelImage):
    config = r'--oem 1 -l eng+tha -c preserve_interword_spaces=1'
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract'
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    labeltext = pytesseract.image_to_string(labelImage, config=config)
    return labeltext

def readQRCode(labelImage):
    decodeObject = pyzbar.decode(labelImage)
    return decodeObject

def getLabelImage(image, verbose=False):
    orig = image.copy()
    # ratio = orig.shape[0] / 500.0
    # image = imutils.resize(image, height=500)

    ############# STEP 1: Edge Detection ######################
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    mask = closing(thresh, square(10))
    mask = erosion(mask, square(5))
    mask = dilation(mask, square(5))
    if verbose:
        plt.imshow(mask)
        plt.show()

    ############# STEP 2: Find contours of paper ######################

    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    label_cnts = []
    label_images = []
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, then we
        # can assume that we have found our label
        if len(approx) == 4:
            label_cnts.append(approx)
            ############## STEP 3: Perspective transform #####################
            label_img = four_point_transform(orig, approx.reshape(4, 2))
            label_images.append(label_img)
    cv2.drawContours(image, label_cnts, -1, (0, 255, 0), 2)
    if verbose:
        plt.imshow(image)
        plt.show()


    return label_images
