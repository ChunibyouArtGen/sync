from sync.server.compute.models.adaptive_st import AdaInModel
from skimage.io import imread, imsave
from skimage import img_as_ubyte
import numpy as np
import sys

adain=AdaInModel(output_img='~/Desktop/',preserve_color=False)
content = sys.argv[1] #'~/Pictures/content.jpg'
style = sys.argv[2]#'~/Pictures/style.jpg'
output = sys.argv[3]#"~/Pictures/output.png"

content_img = imread(content)
style_img =  imread(style)
print("Content shape:{}, dtype {}".format(content_img.shape, content_img.dtype))
print("Style shape:{}, dtype {}".format(style_img.shape, style_img.dtype))
print("Computing...")
res = adain.run({'content': content_img,'style':style_img})
print("Done!")
print("Result shape:{}, dtype {}".format(res.shape, res.dtype))

imsave(output,res)