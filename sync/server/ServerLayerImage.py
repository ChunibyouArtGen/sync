from sync.images import LayerImage
from sync.images import register_image_class
from skimage.io import imsave
import random
import numpy as np

@register_image_class
class ServerLayerImage(LayerImage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = random.randint(1,1000)

    def scan(self):
        # Do nothing
        pass

    def handle_update(self, tile_key, data):
        # Again, do nothing
        pass
    
    def update_tile_data(self, tile_key, data):
        super().update_tile_data(tile_key, data)
        imsave('{}.png'.format(self.key), np.moveaxis(self.data,0,-1))        
    