import cv2
import pdf2image
import numpy as np
from tkinter import filedialog

import pytesseract


class RecipeImage:
    def __init__(self, image, contours):
        self.image = image
        self.contours = contours

class Contour:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

def draw_single_contour_on_image_using_largest_area(image, x, y, w, h):
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


def draw_contours_on_image(image, contours_to_draw):
    for cnt in contours_to_draw:
        cv2.rectangle(image, (cnt.x, cnt.y), (cnt.x + cnt.w, cnt.y + cnt.h), (0, 255, 0), 2)

    return image


def find_horizontal_dotted_lines(contours, img_width, img_height):
    coordinates_and_sizes_dotted_lines = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if round(h / img_height, 2) == 0.01:
            # recipe covers roughly one third of a page
            if round(w / img_width, 2) == 0.31:
                coordinates_and_sizes_dotted_lines.append((x, y, w, h))
                continue

            # recipe covers roughly two third of a page
            if 0.55 <= round(w / img_width, 2) <= 0.56:
                coordinates_and_sizes_dotted_lines.append((x, y, w, h))
                continue

            # recipe covers the whole page
            if round(w / img_width, 2) == 0.85:
                coordinates_and_sizes_dotted_lines.append((x, y, w, h))
                continue

    return coordinates_and_sizes_dotted_lines


def define_rect_values_for_contours_in_header_area(header, contours, max_height):
    new_x = header[0]
    new_y = header[1]
    new_w = header[2]
    new_h = header[3]
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        new_x = min(new_x, x)
        new_y = min(new_y, y)
        new_w = max(new_w, w)
        new_h = max(new_h, y + h)

    if new_h > max_height:
        new_h = max_height

    return (new_x, new_y, new_w, new_h)


# TODO apply pytesseract on single lines of text and not on the whole text
def test_pytesseract_on_part_of_image(part_of_image):
    img_rgb = cv2.cvtColor(part_of_image, cv2.COLOR_BRG2RB)
    return (pytesseract.image_to_string(img_rgb))


def save_pdf_as_images(path):
    pages = pdf2image.convert_from_path(path)
    for i, page in enumerate(pages):
        page.save('pdf_images/pic_' + str(i) + '.jpg', 'JPEG')

def check_if_image_is_bright(image, threshold):
    is_bright = np.mean(image) > threshold
    return True if is_bright else False


def main():
    resize_factor = 2.2

    path = filedialog.askopenfilename()
    img = cv2.imread(path)
    gs_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gs_img, 100, 255, cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (14, 19))
    dilation = cv2.dilate(thresh, rect_kernel, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    dotted_lines = find_horizontal_dotted_lines(contours, thresh.shape[1], thresh.shape[0])

    dict_dotted_line_blocks = dict()

    for (x, y, w, h) in dotted_lines:
        dict_dotted_line_blocks[(x, y, w, h)] = []

        for cnt in contours:
            cnt_x, cnt_y, cnt_w, cnt_h = cv2.boundingRect(cnt)

            if (x <= cnt_x and x + w >= cnt_x + cnt_w) and y <= cnt_y:
                dict_dotted_line_blocks[(x, y, w, h)].append(cnt)

    recipe_parts = []

    for k, v in dict_dotted_line_blocks.items():
        new_x, new_y, new_w, new_h = define_rect_values_for_contours_in_header_area(k, v, img.shape[0])

        part_img = img[new_y:new_y + new_h, new_x:new_x + new_w]
        adapted_contours = []
        for cnt in v:
            cnt_x, cnt_y, cnt_w, cnt_h = cv2.boundingRect(cnt)
            cnt_x = cnt_x - new_x
            cnt_y = cnt_y - new_y

            new_cnt = Contour(cnt_x, cnt_y, cnt_w, cnt_h)
            adapted_contours.append(new_cnt)
        recipe_part = RecipeImage(part_img, adapted_contours)

        recipe_parts.append(recipe_part)

    img_test = draw_contours_on_image(recipe_parts[0].image, recipe_parts[0].contours)
    cv2.imshow('', img_test)
    cv2.waitKey()
    cv2.destroyAllWindows()

    # test_text = test_pytesseract_on_roi_element(part_img)
    # print(test_text)

    # cv2.imshow('', cv2.resize(img_copy, (int(1654/resize_factor), int(2205/resize_factor))))
    # cv2.waitKey()
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
