from PIL import Image
import torch
import numpy as np

from model.infer_model import InferModel
from model.preprocess import *

im = InferModel()
path = "model\\18_em_12_0.bmp"
# path = "model\\download3.jpg"

# img_open = Image.open(path).convert('L')
# print(np.array(img_open))

image = Image.open(path)

converted_image = invertImageColor(image)
resized_image = resizeImage(converted_image)
resized_image.show()
x_t = torch.from_numpy(np.array(resized_image)).type(torch.FloatTensor).squeeze()
# for i in x_t:
#     print(i)
prediction = im.infer(x_t)
print(prediction)
