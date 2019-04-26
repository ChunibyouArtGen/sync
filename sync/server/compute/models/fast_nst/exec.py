import logging
import os
import re
import time

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.onnx
from PIL import Image
from skimage import img_as_ubyte
from skimage.transform import resize
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from .transformer_net import TransformerNet
from .utils import *
from .vgg import Vgg16

logger = logging.getLogger(__name__)


def get_path(key):
    return os.path.join(os.path.dirname(__file__), "models", "{}.pth".format(key))


class FastNSTModel:
    """Class containing implementation of Neural Style Transfer Algorithm"""

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.content_transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Lambda(lambda x: x.mul(255))]
        )

    def run(self, slots):

        """
		Implmentation of Fast Neural Style Transfer Algorithm.Takes Style Image (numpy array with shape (h,w,3)) & 
		Trained Model weights for a particular Style (.pth file) & return output image as a numpy array of shape (3,h,w)
		"""

        content_image = Image.fromarray(np.uint8(slots["content"]))

        content_image = self.content_transform(content_image)
        content_image = content_image.unsqueeze(0).to(self.device)

        with torch.no_grad():
            style_model = TransformerNet()
            path = get_path(slots["style"])
            state_dict = torch.load(path)
            # remove saved deprecated running_* keys in InstanceNorm from the checkpoint
            for k in list(state_dict.keys()):
                if re.search(r"in\d+\.running_(mean|var)$", k):
                    del state_dict[k]
            style_model.load_state_dict(state_dict)
            style_model.to(self.device)
            output = style_model(content_image).cpu()
        res = output.numpy()[0]

        res = np.moveaxis(res, 0, -1)
        if (res > 1).any() or (res < 1).any():
            np.clip(res, -1, 1, res)
            logger.warning("Failed to convert to int. Clipping image!")
        res = resize(res, slots["content"].shape)
        logger.info("resizing to shape {}".format(slots["content"].shape))
        res = img_as_ubyte(res, force_copy=True)
        return res


"""
# Testing model

nst=NeuralStyleTransfer()
content_img_arr = np.asarray(Image.open('<IMAGE PATH>'))
res=nst.run(content_img_arr,'/Models/candy.pth')
print(res)
"""
