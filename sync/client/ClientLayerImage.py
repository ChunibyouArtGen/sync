from ..images import LayerImage
from ..images import register_image_class
from .utils import get_node_object, grab_image
import logging

logger = logging.getLogger(__name__)
import numpy as np
from skimage.io import imsave
import asyncio


@register_image_class
class ClientLayerImage(LayerImage):
    def __init__(self, data_manager, params):
        super().__init__(data_manager, params)

    async def scan(self):
        logger.debug("Scanning image on layer {}".format(
            self.params["layer_name"]))
        # Scan Krita for updates
        self.krita_node = get_node_object(self.params["layer_name"])

        new_data = grab_image(
            self.krita_node,
            self.params["x0"],
            self.params["y0"],
            self.params["x_count"] * self.params["w"],
            self.params["y_count"] * self.params["w"],
        )

        imsave(
            "~/Pictures/celestia/output.png",
            new_data,
        )

        return await self.update_data(new_data)

    def get_image(self):
        return self.data
