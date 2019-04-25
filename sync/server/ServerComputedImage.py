import logging

from sync.images import ComputedImage, register_image_class

logger = logging.getLogger(__name__)


@register_image_class
class ServerComputedImage(ComputedImage):
    def __init__(self, data_manager, params):
        super().__init__(data_manager, params)

        for slot, image in self.slots.items():
            if isinstance(image, str):
                logger.warn(
                    "not connecting string parameter {}:{} as a dependency".format(
                        slot, image
                    )
                )
            self.data_manager.add_dependency(source=image, dependent=self)
