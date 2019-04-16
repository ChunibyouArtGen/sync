#!/usr/bin/python
# -*- coding: utf-8 -*-

from .LayerImage import LayerImage
import numpy as np

from abc import abstractmethod
# from .image_registry import image_class


# @image_class("computed")
class ComputedImage(LayerImage):
    def __init__(self, data_manager, params):
        super().__init__(data_manager, params)
        self.slots = {}
        for slot, uuid in params['inputs'].items():
            source = data_manager.images[uuid]
            self.slots[slot] = source
            data_manager.add_dependency(source=source, dependent=self)

    def get_param_list(self):
        return ["inputs","model_id"] + super().get_param_list()

    @staticmethod
    def get_type():
        return 'computed'

    def get_image(self):
        return self.data

    def recv_computed_image(self, data):
        """
        Receive an updated image from the task runner.
        This function should synchronize with the other side, but does not need to handle any further compute dependencies
        """
        pass
