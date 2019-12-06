import cv2
from DrugLabelScanner import labelscanner
import matplotlib.pyplot as plt


img_path='data/test_5_double.jpg'
img=cv2.imread(img_path)
# img = correct_skew(img,True)
label_images = labelscanner.getLabelImage(img,True)
for label_img in label_images:
    labelscanner.readDrugLabel(label_img)
    qrObject = labelscanner.readQRCode(label_img)
    print(qrObject)
    plt.imshow(label_img)
    plt.show()