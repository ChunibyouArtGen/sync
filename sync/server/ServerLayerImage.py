from sync.images import LayerImage
from sync.images import register_image_class


@register_image_class
class ServerLayerImage(LayerImage):

    def scan(self):
        # Do nothing
        pass

    def handle_update(self, tile_key, data):
        # Again, do nothing
        pass
