import copy
from typing import Union

import cv2
import numpy as np
import pytesseract

DEFAULT_THRESHOLD = 0.01


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


def get_data(row_dimensions, image, configuration=None):
    data = []

    if not configuration:
        configuration = '-c load_system_dawg=false -c load_freq_dawg=false --psm 7'
    else:
        configuration += ' -c load_system_dawg=false -c load_freq_dawg=false --psm 7'

    for row_dimension in row_dimensions:
        text_image = image[row_dimension['top']:row_dimension['bottom'], 0:image.shape[:2][0]]

        # Convert to greyscale, then grab the value
        text_image_gray = cv2.cvtColor(text_image, cv2.COLOR_BGR2GRAY)
        data.append(pytesseract.image_to_string(text_image_gray, config=configuration))

    return data


def parse_and_add_data(data, row_dimensions, key, image, parse_function, configuration=None):
    new_data = parse_function(row_dimensions, image, configuration=configuration)
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
