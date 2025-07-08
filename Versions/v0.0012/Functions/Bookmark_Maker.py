import easyocr
import cv2
from pdf2image import convert_from_path
import numpy as np
from pypdf import PdfReader, PdfWriter
import os


def bookmark_gen(input_pdf, selected_path):
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])
    sent = {}


    img_pg = convert_from_path(input_pdf, dpi= 300)

    cv_imgs = [cv2.cvtColor(np.array(p), cv2.COLOR_RGB2BGR) for p in img_pg]
    img_dim = [img.shape[:2] for img in cv_imgs]


    aoi_list = []
    f = 0
    for img, dim in zip(cv_imgs, img_dim):
        h, w = dim
        aoi_bgr = img[0:int(h * 0.05), 0:w]
        aoi_hsv = cv2.cvtColor(aoi_bgr, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(aoi_hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(aoi_hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)
        kernel = np.ones((2, 2), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)
        aoi_red = cv2.bitwise_and(aoi_hsv, aoi_hsv, mask=mask)
        aoi_list.append(aoi_red)
        cv2.imwrite(f"check{f}.jpg",aoi_red)
        f += 1
    
    reader = easyocr.Reader(['en'])
    for i, aoi in enumerate(aoi_list):
        results = reader.readtext(aoi)
        text_list = []
        for bbox, text, conf in results:
            text_list.append(text)
            sent[i] = " ".join(text_list)   
        

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    for page, bm_title in sent.items():
        writer.add_outline_item(bm_title, page)

    
   
    filename = os.path.splitext(os.path.basename(input_pdf))[0]
    output_path = os.path.join(selected_path, f"{filename}_bm.pdf")
    with open(output_path,"wb") as f:
        writer.write(f)
