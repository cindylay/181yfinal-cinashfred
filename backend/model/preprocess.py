# from matplotlib import pyplot as plt
from PIL import Image, ImageOps
import numpy as np

# import matplotlib


def calculateThreshold(original_image):
    array_of_pixel_color = np.array(original_image.getdata())
    sorted_array = np.sort(array_of_pixel_color)

    total = 0
    for i in range(0, 16):
        total += np.percentile(sorted_array, i)
    average = total // 15

    total_one = 0
    for i in range(76, 101):
        total_one += np.percentile(sorted_array, i)
    average_one = total_one // 25

    total_two = 0
    for i in range(1, 26):
        total_two += np.percentile(sorted_array, i)
    average_two = total_two // 25

    return average


def invertImageColor(original_image):
    image = original_image.convert("L")
    thresh = calculateThreshold(image)

    # got code from https://stackoverflow.com/questions/9506841/using-python-pil-to-turn-a-rgb-image-into-a-pure-black-and-white-image

    fn_one = lambda x: 255 if x > thresh else 0
    image_one = original_image.convert("L").point(fn_one, mode="L")
    rgb_image_one = image_one.convert("RGB")

    fn_two = lambda x: 255 if x < thresh else 0
    image_two = original_image.convert("L").point(fn_two, mode="L")
    rgb_image_two = image_two.convert("RGB")

    if (
        rgb_image_one.getpixel((image_one.size[0] - 1, image_one.size[1] - 1))
        == (0, 0, 0)
        and rgb_image_one.getpixel((image_one.size[0] - 1, 0)) == (0, 0, 0)
        and rgb_image_one.getpixel((0, image_one.size[1] - 1)) == (0, 0, 0)
        and rgb_image_one.getpixel((0, 0)) == (0, 0, 0)
    ):
        return image_one
    elif (
        rgb_image_two.getpixel((image_two.size[0] - 1, image_two.size[1] - 1))
        == (0, 0, 0)
        and rgb_image_two.getpixel((image_two.size[0] - 1, 0)) == (0, 0, 0)
        and rgb_image_two.getpixel((0, image_two.size[1] - 1)) == (0, 0, 0)
        and rgb_image_two.getpixel((0, 0)) == (0, 0, 0)
    ):
        return image_two

    return original_image


def convertToBMP(image):
    image.save("image.bmp")


def resizeImage(image):
    average_area = 36881  # summed area of all trainig data images // number of images
    current_image_area = image.size[0] * image.size[1]

    scale_percent = np.sqrt(current_image_area / average_area)

    resized_image = image.resize(
        (
            round(image.size[0] * (1 / scale_percent)),
            round(image.size[1] * (1 / scale_percent)),
        )
    )
    return resized_image


# if __name__ == '__main__':
#     image = Image.open("18_em_6_0.bmp")
#     # calculateThreshold(image)
#     # colorized_image = ImageOps.colorize(image, black ="black", white ="white")
#     # colorized_image.show()
#     converted_image = invertImageColor(image)
#     converted_image.show()
#     resized_image = resizeImage(converted_image)
#     # resized_image.show()
#     # convertToBMP(resized_image)
