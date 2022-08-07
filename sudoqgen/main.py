import os
import random

from . import augmentation, draw, generate, utils

augm_funcs = [
    (augmentation.Functions.bgr2gray, 0.2),
    (augmentation.Functions.blur, 0.5),
    (augmentation.Functions.noise, 0.5),
    (augmentation.Functions.random_lines, 0.5),
]

texture_folder = "./textures/"
output_folder = "./output/"

if not os.path.exists(output_folder):
    os.mkdir(output_folder)


def main(num_gen, image_size, sudoku_size):
    augm = augmentation.Augmentation(augm_funcs)

    for _ in range(num_gen):
        data = generate.generate_sudoku(difficulty=random.randint(30, 64))
        image_data = draw.draw(
            data,
            image_size,
            sudoku_size,
            texture_folder=texture_folder,
        )
        # rotate the generated sudoQ grid
        augmentation.Functions.rotate(image_data)

        # fill in the white gaps with a random texture
        draw.apply_background_image(image_data, texture_folder)

        augm(image_data)

        utils.save_image_data(image_data, output_folder)


if __name__ == "__main__":
    # need to parse args
    main(20, (1024, 1024), (512, 512))
