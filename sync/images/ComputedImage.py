#!/usr/bin/python
# -*- coding: utf-8 -*-

from .LayerImage import LayerImage
import numpy as np

from abc import abstractmethod
# from .image_registry import image_class
import logging
logger = logging.getLogger(__name__)

# @image_class("computed")
class ComputedImage(LayerImage):
    def __init__(self, data_manager, params):
        super().__init__(data_manager, params)
        self.slots = {}
        for slot, uuid in params['inputs'].items():
            try:
                source = data_manager.images[uuid]
                self.slots[slot] = source
            except:
                logger.warn("Failed to decode input {}:{}, leaving as-is".format(slot, uuid))
                self.slots[slot] = uuid
                

    def get_param_list(self):
        return ["inputs","model_id"] + super().get_param_list()

    @staticmethod
    def get_type():
        return 'computed'

    def get_image(self):
        return self.data

    def get_slots(self):
        return self.slots
    
    async def register_self(self):
        super().register_self()
        for slot, image in self.params['inputs'].items():
            self.data_manager.add_dependency(source=image, dependent=self)
