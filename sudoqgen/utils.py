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
