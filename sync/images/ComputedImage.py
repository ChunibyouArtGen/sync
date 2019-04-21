#!/usr/bin/python
# -*- coding: utf-8 -*-

from .LayerImage import LayerImage
import numpy as np

from abc import abstractmethod
from copy import deepcopy
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
        print(params)
        for slot, image in params['inputs'].items():
            params['inputs'][slot] = self.data_manager.reverse[image]
        
        return params        
