image_classes = {}


def register_image_class(cls):
    image_classes[cls.get_type()] = cls
    return cls
