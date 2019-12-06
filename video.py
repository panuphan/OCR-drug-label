# import the necessary packages
from __future__ import print_function

import math
import time
import cv2
from skimage.morphology import dilation, erosion, closing,square

from DrugLabelScanner import labelscanner


def get_mask(image):
    ret, thresh = cv2.threshold(image, 20, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    mask = closing(thresh, square(10))
    mask = erosion(mask, square(5))
    mask = dilation(mask,square(5))
    return mask

def get_labelImage(image,mask):
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour = max(contours, key=lambda cnt:cv2.contourArea(cnt))
    cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
    rect = cv2.minAreaRect(contour)
    center, size, theta = rect
    # Convert to int
    center, size = tuple(map(int, center)), tuple(map(int, size))
    # Get rotation matrix for rectangle
    M = cv2.getRotationMatrix2D( center, theta, 1)
    # Perform rotation on src image
    sq = int(math.sqrt(int(image.shape[0]**2+size[1]**2)))
    dst = cv2.warpAffine(image, M, (sq,sq))
    out = cv2.getRectSubPix(dst,size, center)
    if out.shape[0]>out.shape[1]:
        out=cv2.transpose(out)
        out=cv2.flip(out,flipCode=0)
    return out

# initialize the camera and stream
print("[INFO] sampling THREADED frames from `camera` module...")
vs = cv2.VideoCapture(1)
time.sleep(2.0)
while True:
    _,frame = vs.read()
    # frame = imutils.resize(frame, width=400)
    label_images = labelscanner.getLabelImage(frame)
    qr = None
    for label_img in label_images:
        labelscanner.readDrugLabel(label_img)
        qrObject = labelscanner.readQRCode(label_img)
        if len(qrObject) > 0:
            qr = str(qrObject[0].data)
            print(str(qrObject[0].data))
    if qr is not None:
        cv2.putText(frame, qr, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # check to see if the frame should be displayed to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# do a bit of cleanup
cv2.destroyAllWindows()