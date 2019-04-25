#!/usr/bin/python
# -*- coding: utf-8 -*-

from .layer_image import LayerImage
import numpy as np

from abc import abstractmethod
from copy import deepcopy
# from .image_registry import image_class
import logging
from sync.images import Image

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
                logger.warn("Input {}:{} is not a valid uuid, leaving as-is".format(slot, uuid))
                self.slots[slot] = uuid
                

    def get_param_list(self):
        return ["inputs","model_key"] + super().get_param_list()

    @staticmethod
    def get_type():
        return 'computed'

    def get_image(self):
        return self.data

    def get_slots(self):
        return self.slots
    
    
    def get_params(self):
        params = self.params.copy()
        
        for slot, image in params['inputs'].items():
            if isinstance(params['inputs'][slot], Image):
                params['inputs'][slot] = self.data_manager.reverse[image]
        print(params)
        return params        
