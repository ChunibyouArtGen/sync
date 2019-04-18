from sync.images import ComputedImage
from sync.images import register_image_class
import logging

logger = logging.getLogger(__name__)

@register_image_class
class ServerComputedImage(ComputedImage):
    def __init__(self, data_manager, params):
        super().__init__(data_manager, params)


    def handle_computed_image(self, data):
        """
        Receive an updated image from the task runner.
        This function should synchronize with the other side, but does not need to handle any further compute dependencies
        """
        logger.info("ComputedImage recieved computed data. Processing...")
        self.update_data(data)
