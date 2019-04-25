import random

import numpy as np

from skimage.io import imsave
from sync.images import LayerImage, register_image_class


@register_image_class
class ServerLayerImage(LayerImage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = random.randint(1, 1000)

    def scan(self):
        # Do nothing
        pass

    def update_tile_data(self, tile_key, data):
        super().update_tile_data(tile_key, data)
        imsave("{}.png".format(self.params["layer_name"]), self.data)
