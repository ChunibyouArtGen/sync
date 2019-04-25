from .image_registry import image_classes, register_image_class
from .image import Image
from .computed_image import ComputedImage
from .layer_image import LayerImage

def load_image_definition(image_dict, data_manager):
    cls = image_classes[image_dict["type"]]
    return cls(**image_dict, data_manager=data_manager)


__all__ = [
    "image_classes", "ComputedImage", "LayerImage", 'register_image_class', 'Image'
]
