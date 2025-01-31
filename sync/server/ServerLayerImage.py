from sync.images import LayerImage
from sync.images import register_image_class
from skimage.io import imsave
import random
import numpy as np

@register_image_class
class ServerLayerImage(LayerImage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def scan(self):
        # Do nothing
        pass

    
    def update_tile_data(self, tile_key, data):
        super().update_tile_data(tile_key, data)
        imsave('~/Pictures/celestia/{}.png'.format(self.params['layer_name']), self.data)        
    