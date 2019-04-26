import numpy as np
from skimage import img_as_ubyte
from skimage.io import imread, imsave

from sync.server.compute.models.adaptive_st import AdaInModel

adain = AdaInModel(output_img="/home/ashik/Desktop/", preserve_color=False)

content_img = imread("~/Pictures/content.jpg")
style_img = imread("~/Pictures/style.jpg")
print("Content shape:{}, dtype {}".format(content_img.shape, content_img.dtype))
print("Style shape:{}, dtype {}".format(style_img.shape, style_img.dtype))
print("Computing...")
res = adain.run({"content": content_img, "style": style_img})
print("Done!")
print("Result shape:{}, dtype {}".format(res.shape, res.dtype))

imsave("~/Pictures/output.png", res)
