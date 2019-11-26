import cv2
import numpy as np
from skew_correction.skewer import Skewer

def skewCorrection(img_path):
    img=cv2.imread(img_path)
    # orig=img.copy()
    # img=cv2.resize(img,None,fx=0.5,fy=0.5)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    # img = cv2.Canny(img, 10, 50)

    skewer = Skewer(image_data=img)
    rotated = skewer.get_rotated()

    if skewer.is_rotated(): # Returns true or false according to any skew operation
        cv2.imshow("Rotated image", rotated)
        cv2.imshow("image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
def correct_skew(img_path,verbose=False):
    image = cv2.imread(img_path)
    # image = cv2.resize(image,None,fx=0.5,fy=0.5)
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
