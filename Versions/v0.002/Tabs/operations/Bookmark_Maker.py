import easyocr
import cv2
import numpy as np

from pdf2image import convert_from_path
from pypdf import PdfReader, PdfWriter

class BookMark():
    def bookmark_gen(self, input_pdf, progress_callback = None):

        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([179, 255, 255])
        bm = {}

        img_pg = convert_from_path(input_pdf, dpi= 300)

        cv_imgs = [cv2.cvtColor(np.array(p), cv2.COLOR_RGB2BGR) for p in img_pg]
        img_dim = [img.shape[:2] for img in cv_imgs]
        total_pages = len(cv_imgs)

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
            f += 1
            if progress_callback:
                progress_callback(int((f + 1) / total_pages * 100)*50)   
        
        reader = easyocr.Reader(['en'])
        for i, aoi in enumerate(aoi_list):
            results = reader.readtext(aoi)
            text_list = []
            for bbox, text, conf in results:
                text_list.append(text)
                bm[i] = " ".join(text_list)
            if progress_callback:
                progress_callback(int(50+((i + 1) / total_pages )* 50))   
        return bm
    
    def read_bookmarks(self, outlines, parent_title=None, bookmark_list=None, progress_callback=None):
        if bookmark_list is None:
            bookmark_list = []

        i = 0
        total_bookmarks = len(outlines)

        while i < total_bookmarks:
            item = outlines[i]

            if isinstance(item, list):
                self.read_bookmarks(item, parent_title, bookmark_list, progress_callback)
                i += 1
                continue

            try:
                if self.reader.get_destination_page_number(item) or self.reader.get_destination_page_number(item) == 0:
                    page_num = self.reader.get_destination_page_number(item) + 1
                else:
                    page_num = 999999999+i
                
                bookmark_list.append([{page_num: item.title}, parent_title])
            except Exception as e:
                print(f"Error processing bookmark '{getattr(item, 'title', 'Unknown')}': {e}")

            # Check for children
            if i + 1 < total_bookmarks and isinstance(outlines[i + 1], list):
                self.read_bookmarks(outlines[i + 1], parent_title=item.title, bookmark_list=bookmark_list, progress_callback=progress_callback)
                i += 2
            else:
                i += 1

            if progress_callback:
                progress_callback(((i + 1) / total_bookmarks) * 100)

        return bookmark_list

    def read_pdf(self, input_pdf_path, progress_callback = None):
        self.reader = PdfReader(input_pdf_path)
        outlines = self.reader.outline
        len(outlines)
        bm_list = self.read_bookmarks(outlines, progress_callback=progress_callback)
        return bm_list



    def output_pdf(self, data, input_pdf_path, output_path):
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        def read_recursion(items, depth=0, parent_outline=None):
            for branch in items:
                title = branch['title']
                page = branch['page']

                #assert isinstance(page, int), f"Expected int for page, got {type(page)}"
                current_outline = writer.add_outline_item(title, page, parent=parent_outline)

                if branch.get('children'):
                    read_recursion(branch['children'], depth + 1, parent_outline=current_outline)

        read_recursion(data)

        with open(output_path, "wb") as f:
            writer.write(f)