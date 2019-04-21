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
        if params['layer_name'] not in ['', None, ' ']:
            self.krita_node = get_node_object(params['layer_name'])


    def update_tile_data(self, tile_key, data):
        super().update_tile_data(tile_key,data)

        logger.info("Writing data to krita...")
        if self.krita_node:
            x0 = self.params['x0']
            y0 = self.params['y0']
            x = self.params['w'] * self.params['x_count']
            y = self.params['w'] * self.params['y_count']
            #image = np.ones((x,y,4))*254
            #image[:,:,:3] = self.data
            image=data
            self.krita_node.setPixelData(image.ravel().tobytes(), x0, y0, x, y)
            imsave("~/Pictures/output.png", data)
        else:
            logger.warn('Not rendering!')
    
    async def scan(self):
        pass
    
