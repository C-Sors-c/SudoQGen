import math

import cv2
import numpy as np

from . import utils


def get_function_by_name(name: str):
    """Get the function by name.

    Args:
        name (str): the name of the function.

    Returns:
        function: the function.
    """
    return getattr(Functions, name)


class Functions:
    """Class containing every augmentation functions"""

    def bgr2gray(image_data: dict):
        image_data["image"] = cv2.cvtColor(cv2.cvtColor(image_data["image"], cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

    def blur(image_data: dict):
        image_data["image"] = cv2.blur(image_data["image"], (3, 3))

    def noise(image_data: dict):
        scale = 25
        noise = np.random.randint(-scale, scale, size=image_data["image"].shape)
        image_data["image"] = image_data["image"] + (image_data["image"] < 255 - scale) * noise

    def random_lines(image_data: dict):
        n_lines = np.random.randint(2, 4)
        for _ in range(n_lines):
            p1 = (
                np.random.randint(0, image_data["image"].shape[1]),
                np.random.randint(0, image_data["image"].shape[0]),
            )
            p2 = (
                np.random.randint(0, image_data["image"].shape[1]),
                np.random.randint(0, image_data["image"].shape[0]),
            )

            rdm_color = (
                np.random.randint(0, 255),
                np.random.randint(0, 255),
                np.random.randint(0, 255),
            )
            image_data["image"] = cv2.line(
                image_data["image"],
                p1,
                p2,
                rdm_color,
                1,
                cv2.LINE_AA,
            )

    def rotate(image_data: dict, depth=1.25):
        height, width, _ = image_data["image"].shape

        x = np.random.randint(-30, 30)
        y = np.random.randint(-30, 30)
        z = np.random.randint(-15, 15)

        ax = float(x * (math.pi / 180.0))
        ay = float(y * (math.pi / 180.0))
        az = float(z * (math.pi / 180.0))

        trans = np.eye(4)
        trans[2, 3] = depth

        inv_trans = np.eye(4)
        inv_trans[2, 3] = 1 / depth

        # projection + normalization to [-1, 1]
        proj2dto3d = np.array(
            [
                [1 / width, 0, -1 / 2],
                [0, 1 / height, -1 / 2],
                [0, 0, 0],
                [0, 0, 1],
            ],
            np.float32,
        )

        # projection + normalization to [0, width || height]
        proj3dto2d = np.array(
            [
                [width, 0, width / 2, 0],
                [0, height, height / 2, 0],
                [0, 0, 1, 0],
            ],
            np.float32,
        )

        rx = np.eye(4)
        rx[1, 1] = math.cos(ax)
        rx[1, 2] = -math.sin(ax)
        rx[2, 1] = math.sin(ax)
        rx[2, 2] = math.cos(ax)

        ry = np.eye(4)
        ry[0, 0] = math.cos(ay)
        ry[0, 2] = -math.sin(ay)
        ry[2, 0] = math.sin(ay)
        ry[2, 2] = math.cos(ay)

        rz = np.eye(4)
        rz[0, 0] = math.cos(az)
        rz[0, 1] = -math.sin(az)
        rz[1, 0] = math.sin(az)
        rz[1, 1] = math.cos(az)

        rot = rx.dot(ry).dot(rz)
        inv_rot = utils.transpose(rot)

        final = proj3dto2d @ trans @ rot @ proj2dto3d

        # calculate the inverse matrix of final rotations
        # we will need to do that from scratch but since we have rotation matrix, it should be fine
        inv_final = np.linalg.inv(final)

        # inv_final = proj3dto2d @ inv_rot @ inv_trans @ proj2dto3d #not working for the moment

        utils.warpPerspective(image_data, inv_final, dst_shape=(height, width, 3))

        # update the transform matrix
        image_data["transform-matrix"] = final @ image_data["transform-matrix"]
        utils.create_grid_array(image_data)


class Augmentation:
    def __init__(self, funcs=[]):
        """Init the Augmentation function class

        Args:
            additionnal_funcs (list(tuple(method, float)), optional): tuple containing the function and the frequency.
        """

        self.functions = funcs

    def __call__(self, image_data: dict):
        """When called, apply every randomly every augmentation functions

        Args:
            image_data (dict): dict containing the image and its data
        """
        for (func, freq) in self.functions:
            try:
                rdm = np.random.uniform()
                if rdm < freq:
                    func(image_data)
            except Exception as e:
                print(f"Error in augmentation function: {e}")
