import os
import random
from glob import glob

import cv2
import numpy as np

from . import utils

fonts = [
    cv2.FONT_HERSHEY_SIMPLEX,
    cv2.FONT_HERSHEY_PLAIN,
    cv2.FONT_HERSHEY_DUPLEX,
    cv2.FONT_HERSHEY_COMPLEX,
    cv2.FONT_HERSHEY_TRIPLEX,
    cv2.FONT_HERSHEY_COMPLEX_SMALL,
    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
]


def get_optimal_font_scale(text, width, font):
    for scale in reversed(range(0, 60, 1)):
        textSize = cv2.getTextSize(text, fontFace=font, fontScale=scale / 10, thickness=1)
        new_width = textSize[0][0]
        if new_width <= width:
            return scale / 10
    return 1


def draw(
    data: dict,
    image_size: (int, int),
    sudoku_size: (int, int),
    color=(0, 0, 0),
    font_thickness=1,
    line_thickness=1,
    texture_folder="./textures/",
):
    """Sudoku draw function

    Args:
        data (dict): dict containing the sudoku grid
        image_size (int, int): size of the final image
        sudoku_size (int, int): size of the sudoku grid in the image
        color (tuple, optional): the color the sudoku are being drawn. Defaults to (0, 0, 0).
        font_thickness (int, optional): thickness of the font. Defaults to 1.
        line_thickness (int, optional): thickness of the lines. Defaults to 1.
        texture_folder (str, optional): folder containing the background textures. Defaults to "".

    Returns:
        dict: image_data dict containing the image and its labels
    """
    sudoku = data["sudoku"]
    side = sudoku.shape[0]

    # pick a random texture from texture folder
    texture_folder = os.path.normpath(texture_folder)
    if os.path.exists(texture_folder):
        textures_path = glob(os.path.join(texture_folder, "*"))
        rdm_texture_path = random.choice(textures_path)
        image = cv2.imread(rdm_texture_path)
        image = cv2.resize(image, image_size)
    else:
        image = np.full((image_size[0], image_size[1]), 255, dtype=np.uint8)

    (grid_w, grid_h) = (
        sudoku_size[0],
        sudoku_size[1],
    )
    (xpos, ypos) = (
        random.randint(0, image_size[0] - grid_w),
        random.randint(0, image_size[1] - grid_h),
    )
    (cell_w, cell_h) = (
        grid_w / side,
        grid_h / side,
    )

    # vertical lines
    for i in range(side + 1):
        p1 = (int(xpos + i * cell_w), int(ypos))
        p2 = (int(xpos + i * cell_w), int(ypos + sudoku_size[1]))
        image = cv2.line(image, p1, p2, color, line_thickness)

    # horizontal lines
    for j in range(side + 1):
        p1 = (int(xpos), int(ypos + j * cell_h))
        p2 = (int(xpos + sudoku_size[0]), int(ypos + j * cell_h))
        image = cv2.line(image, p1, p2, color, line_thickness)

    for i in range(side):
        for j in range(side):
            num = int(sudoku[i][j])
            if num == 0:
                continue

            text = str(num)
            rdm_text_scale = np.random.uniform(0.5, 1)

            font = random.choice(fonts)
            p = (
                int(xpos + (((1 - rdm_text_scale) / 2 + 0.1) * cell_w) + i * cell_w),
                int(ypos + ((0.9 - (1 - rdm_text_scale) / 2) * cell_h) + j * cell_h),
            )
            font_scale = get_optimal_font_scale(text, cell_w, font) * 0.8 * rdm_text_scale

            image = cv2.putText(
                image,
                text,
                p,
                font,
                font_scale,
                color,
                font_thickness,
                cv2.LINE_AA,
            )

    translation = np.array([[1, 0, xpos], [0, 1, ypos], [0, 0, 1]])
    scale = np.array([[cell_w, 0, 0], [0, cell_h, 0], [0, 0, 1]])
    rotation = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    data["transform-matrix"] = translation @ scale @ rotation
    utils.create_grid_array(data)

    data["image"] = image
    return data


def apply_background_image(image_data, texture_folder, mask_values=[255, 255, 255]):
    texture_folder = os.path.normpath(texture_folder)
    if os.path.exists(texture_folder):
        textures_path = glob(os.path.join(texture_folder, "*"))
        rdm_texture_path = np.random.choice(textures_path)
        back = cv2.imread(rdm_texture_path)
        back = cv2.resize(back, (image_data["image"].shape[1], image_data["image"].shape[0]))
    else:
        back = np.random.randint(0, 255, image_data["image"].shape, dtype=np.uint8)

    # create the mask
    mask = image_data["image"] == mask_values
    # apply the texture on the mask
    image_data["image"][mask] = back[mask]
