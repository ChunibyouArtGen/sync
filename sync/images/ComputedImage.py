#!/usr/bin/python
# -*- coding: utf-8 -*-

from .Image import Image

# from .image_registry import image_class


# @image_class("computed")
class ComputedImage(Image):
    def __init__(self, data_manager, **params):
        assert 'inputs' in params
        assert 'model_id' in params

        super().__init__(data_manager, params)

    def get_definition(self):
        return {
            "inputs": self.params['inputs'],
            "model_id": self.params['model_id']
        }

    @staticmethod
    def get_type():
        return 'computed'