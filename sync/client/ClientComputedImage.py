from sync.images import ComputedImage
from sync.images import register_image_class
from .utils import get_node_object
import numpy as np
import logging

logger = logging.getLogger(__name__)
from skimage.io import imsave


@register_image_class
class ClientComputedImage(ComputedImage):
    def __init__(self, data_manager, params):
        super().__init__(data_manager, params)
        if params["layer_name"] not in ["", None, " "]:
            self.krita_node = get_node_object(params["layer_name"])

    def update_tile_data(self, tile_key, data):
        super().update_tile_data(tile_key,data)
        if self.krita_node:
            x0,y0 = self.get_tile_coords(tile_key)
            w = self.params['w']
            alpha = np.full((self.params['w'],self.params['w'],1), 254, dtype=np.uint8)
            
            image = np.concatenate((data,alpha),axis=-1).astype(np.uint8)
            image = np.flip(np.roll(image,1,axis=-1),axis=-1)
            
            self.krita_node.setPixelData(image.tobytes(), y0, x0, w, w)
            imsave("~/Pictures/celestia/output.png", self.data)

    async def scan(self):
        pass
