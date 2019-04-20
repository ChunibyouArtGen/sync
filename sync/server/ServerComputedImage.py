from sync.images import ComputedImage
from sync.images import register_image_class
import logging

logger = logging.getLogger(__name__)

@register_image_class
class ServerComputedImage(ComputedImage):
    def __init__(self, data_manager, params):
        super().__init__(data_manager, params)


    async def register_self(self):
        super().register_self()
        for slot, image in self.params['inputs'].items():
            self.data_manager.add_dependency(source=image, dependent=self)


    def handle_update(self, data):
        self.data = data