import requests
from PIL import Image, ImageDraw, ImageFont
import random
import os
from config import GOOGLE_FONTS_API_KEY


def get_random_font():
    # Get a list of fonts from the Google Fonts API
    fonts = requests.get("https://www.googleapis.com/webfonts/v1/webfonts?key=" +
                         GOOGLE_FONTS_API_KEY + "&sort=popularity").json()

    # Choose a random font from the list
    font = random.choice(fonts["items"])
    # Choose a random variant of the font
    variant = random.choice(font["variants"])

    # Download the font file
    font_url = "https://fonts.googleapis.com/css?family={}:{}".format(
        font["family"], variant)
    font_file = requests.get(font_url).text.split("url(")[1].split(")")[0]
    # Return the font file
    return font_file


def generate_dataset(n):
    # for i in range(n):
    #     # Generate a random font
    #     font = get_random_font()
    #     # download the font file
    #     font = requests.get(font).content
    #     # save the font file
    #     with open("fonts/" + str(i) + ".ttf", "wb") as f:
    #         f.write(font)
    #     # Generate a random font size
    #     font_size = random.randint(10, 14)
    #     # Generate a random digit from 0 to 9
    #     text = str(random.randint(0, 9))
    #     # Generate a random rotation
    #     rotation = random.randint(-180, 180)
    #     # Generate a position for the text depending on the font size
    #     position = (random.randint(10, 28 - font_size),
    #                 random.randint(10, 28 - font_size))
    #     img = Image.new("RGB", (28, 28), color=(255, 255, 255))
    #     draw = ImageDraw.Draw(img)

    #     try:
    #         draw.text(position, text, font=ImageFont.truetype(
    #             "fonts/" + str(i) + ".ttf", font_size), fill=(0, 0, 0))
    #     except:
    #         os.remove("fonts/" + str(i) + ".ttf")
    #         continue
    #     image = img.rotate(rotation)

    #     image.save("out/" + str(text) + "_" + str(i) + ".png")

    #     os.remove("fonts/" + str(i) + ".ttf")

    for i in range(n//10):
        # save white images
        img = Image.new("RGB", (28, 28), color=(255, 255, 255))
        # add a random number of black pixels
        for j in range(random.randint(0, 50)):
            x = random.randint(0, 27)
            y = random.randint(0, 27)
            img.putpixel((x, y), (0, 0, 0))

        img.save("out/" + "blank_" + str(i) + ".png")


# create the out folder
if not os.path.exists("out"):
    os.mkdir("out")

# create the fonts folder
if not os.path.exists("fonts"):
    os.mkdir("fonts")

# Generate a dataset of 25,000 images
generate_dataset(25000)
