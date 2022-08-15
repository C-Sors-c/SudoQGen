import json
import os
import time

import cv2
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    """Special json encoder for numpy types"""

    def default(self, obj):
        if isinstance(
            obj,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),
        ):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def save_image_data(image_data: dict, dataset_folder: str):
    """Save an image along with it's labels in a json file.

    Args:
        image_data (dict): dict containing the image and the labels.
        dataset_folder (str): where to save the image and the labels.
    """
    image = image_data["image"]
    del image_data["image"]

    filepath = os.path.join(dataset_folder, str(time.time()))
    cv2.imwrite(filepath + ".png", image)

    with open(filepath + ".json", "w") as json_file:
        json.dump(image_data, json_file, cls=NumpyEncoder)


def crop_image(image, p1, p2):
    """Crop an image.

    Args:
        image (numpy.ndarray): the image to crop.
        p1 (tuple): the first point of the rectangle to crop.
        p2 (tuple): the second point of the rectangle to crop.
    """
    return image[p1[1] : p2[1], p1[0] : p2[0]]


def get_point_transform(image_data, x, y):
    """Get the point on the grid at the given coordinates.

    Args:
        image_data (dict): the image data.
        x (int): the x coordinate.
        y (int): the y coordinate.

    Returns:
        tuple: the point on the grid at the given coordinates.
    """

    p = image_data["transform-matrix"] @ np.array([x, y, 1])
    p /= p[2]
    p = p.astype(np.int32)
    return p


def create_grid_array(image_data):
    """Create the grid coordinates array.

    Args:
        image_data (dict): the image data.
    """

    # create a 10x10x2 array to contain the coordinates of the sudoku grid
    image_data["grid"] = np.zeros((10, 10, 3), np.int32)

    for x in range(10):
        for y in range(10):
            p1 = get_point_transform(image_data, x, y)
            image_data["grid"][x, y, :] = p1


def transpose(matrix):
    """Transpose a matrix.

    Args:
        matrix (np.array): the matrix to be transposed.
    """
    transposed = np.zeros((matrix.shape[1], matrix.shape[0]))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            transposed[j, i] = matrix[i, j]
    return transposed


def warpPerspective(image_data, inv_transform_matrix, dst_shape=(1024, 1024, 3)):
    """Warp perspective function from "scratch".

    Args:
        image_data (dict): Image data dictionary.
        inv_transform_matrix (np.array): inverse of the transform matrix (dst -> src).
        dst_shape (tuple, optional): Destination image shape. Defaults to (1024, 1024, 3).
    """
    # knowned issues with dst_shape not centering the image,
    # will need to fix that in the projection / normalization matrix step.

    image = image_data["image"]

    height, width, _ = image.shape
    dst = np.full(dst_shape, 0, dtype=np.uint8)

    for y in range(dst_shape[0]):
        for x in range(dst_shape[1]):
            p = inv_transform_matrix @ np.array([x, y, 1])
            p /= p[2]

            if 0 <= p[0] < width - 1 and 0 <= p[1] < height - 1:
                dst[y, x, :] = image[round(p[1]), round(p[0]), :]

    image_data["image"] = dst
