#!/usr/bin/python
# -*- coding: utf-8 -*-

from .LayerImage import LayerImage
import numpy as np

# from .image_registry import image_class


# @image_class("computed")
class ComputedImage(LayerImage):
    def __init__(self, data_manager, task_runner, params):
        super().__init__(data_manager, params)
        self.task_runner = task_runner
        self.data = np.zeros((params['width'], params['height'], 3))
        inputs = params['inputs']
        for slot, uuid in inputs.items():
            inputs[slot] = self.data_manager.images[uuid]
        self.inputs = inputs

    def get_params(self):
        return ["inputs", "model_id", 'width', 'height']

    @staticmethod
    def get_type():
        return 'computed'

    def get_image(self):
        return self.data
