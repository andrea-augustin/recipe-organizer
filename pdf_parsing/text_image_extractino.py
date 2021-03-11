import textract
import cv2
import pdf2image
import numpy as np
from tkinter import filedialog

from collections import Counter


def save_pdf_as_images(path):
    pages = pdf2image.convert_from_path(path)
    for i, page in enumerate(pages):
        page.save('pdf_images/pic_' + str(i) + '.jpg', 'JPEG')


def extract_text_from_pdf_with_textract(path):
    # gets the text from the pdf but scrambles up the order of the text (or what the expected order of the text is
    # supposed to be...)
    text = textract.process(path)
    text = text.decode("utf-8")

    return text


def count_pixel_colors_in_image(image):
    counter_pixel_color = Counter()

    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            pixel = image[i, j]

            counter_pixel_color.update([tuple(pixel)])

    return len(counter_pixel_color)


def check_if_image_is_bright(image, threshold):
    is_bright = np.mean(image) > threshold
    return True if is_bright else False


def mark_text_fields_in_image(path):
    image = cv2.imread(path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([0,0,218])
    upper = np.array([157, 54, 255])
    mask = cv2.inRange(hsv, lower, upper)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate = cv2.dilate(mask, kernel, iterations=1)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        ar = w / float(h)
        if ar < 5:
            cv2.drawContours(dilate, [c], -1, (0,0,0), -1)

    result = 255 - cv2.bitwise_and(dilate, mask)

    cv2.imshow('', cv2.resize(mask, (int(1654/2), int(2205/2))))
    cv2.waitKey()


def extract_text_from_image(path):
    check_dilation = False

    img = cv2.imread(path)

    amount_colors = count_pixel_colors_in_image(img)

    gs_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_img = cv2.GaussianBlur(gs_img, (3,3), 0)

    threshold = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    rectangular_thingie = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilation = cv2.dilate(threshold, rectangular_thingie, iterations=5)

    if check_dilation:
        cv2.imshow('', cv2.resize(dilation, (int(1654/2), int(2205/2))))
        cv2.waitKey()

    contours = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    ROI_number = 0
    for c in contours:
        area = cv2.contourArea(c)

        if area < 1000:
            continue

        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 3)
        ROI = img[y:y+h, x:x+w]

        amount_colors_in_ROI = count_pixel_colors_in_image(ROI)

        #if amount_colors_in_ROI > amount_colors * 0.9 or amount_colors_in_ROI < 100:
        #    continue

        cv2.imwrite('roi_images/ROI_{}.png'.format(ROI_number), ROI)
        ROI_number += 1


if __name__ == '__main__':
    extract_text_from_image(filedialog.askopenfilename())
