import copy
import os
import platform
from typing import Union

import cv2
import numpy as np
import pytesseract

DEFAULT_THRESHOLD = 0.01
DEFAULT_WHITELIST = '"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 "'


def find_image(small_image: Union[str, np.ndarray], large_image: Union[str, np.ndarray],
               threshold: float = DEFAULT_THRESHOLD, display: bool = False):
    matches = []

    if isinstance(small_image, str):
        small_image = cv2.imread(small_image)

    if isinstance(large_image, str):
        large_image = cv2.imread(large_image)

    result = cv2.matchTemplate(small_image, large_image, cv2.TM_SQDIFF_NORMED)

    locations = np.where(result <= threshold)
    for point in zip(*locations[::-1]):
        matches.append(point)

    if display and matches:
        scratch_image = copy.deepcopy(large_image)
        for point in matches:
            cv2.rectangle(scratch_image, point, (point[0] + small_image.shape[:2][1], point[1] + small_image.shape[:2][0]), (0, 0, 255), 2)

        show_image(scratch_image)

    return matches


def get_data(row_dimensions, image, whitelist=None):
    data = []

    for index, row_dimension in enumerate(row_dimensions):
        text_image = image[row_dimension['top']:row_dimension['bottom'], 0:image.shape[:2][0]]

        data.append(get_line(text_image, whitelist=whitelist))

    return data


def get_line(text_image, whitelist=None):
    if not whitelist:
        whitelist = DEFAULT_WHITELIST

    # Utilize the customized trained data file for Villagers & Heroes fonts
    # Remove the dictionaries as we are trying to parse fantasy names
    # Add a whitelist of characters
    # Change the page segmentation mode to "7 - Treat the image as a single text line."
    configuration = '-l vnh ' \
                    '-c load_system_dawg=false ' \
                    '-c load_freq_dawg=false ' \
                    '-c tessedit_char_whitelist={} ' \
                    '--psm 7'.format(whitelist)

    # Convert to greyscale, then grab the value
    text_image_gray = cv2.cvtColor(text_image, cv2.COLOR_BGR2GRAY)

    return pytesseract.image_to_string(text_image_gray, config=configuration)


def parse_and_add_data(data, row_dimensions, key, image, parse_function, whitelist=None):
    new_data = parse_function(row_dimensions, image, whitelist=whitelist)
    if not data:
        for i in range(0, len(new_data)):
            data.append({})
    for index, value in enumerate(new_data):
        data[index][key] = value


def show_image_selection(image, left, right, top, bottom):
    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

    show_image(image)


def show_image(image):
    # Display the original image with the rectangle around the match.
    cv2.imshow('output', image)

    # The image is only displayed if we call this
    cv2.waitKey(0)


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """

    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
