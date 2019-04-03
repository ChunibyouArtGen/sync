#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from .Image import Image
from ..data_manager import DataManager

# from .image_registry import image_class


# @image_class("layer")
class LayerImage(Image):
    def __init__(self, data_manager: DataManager, params):
        super().__init__(data_manager, params)
        self.data = np.zeros(
            (params['x'] * params['w'], params['y'] * params['w'], 3))

    def get_param_list(self):
        return [
            "layer_name",
            "x0",
            "y0",
            "x",
            "y",
            "w",
        ]

    @staticmethod
    def get_type():
        return 'layer'

    def get_tile_key(self, x, y):
        x_pos = (x - self.params['x0']) / self.params['w']
        y_pos = (y - self.params['y0']) / self.params['w']
        assert 0 <= x_pos < self.params['x']
        assert 0 <= y_pos < self.params['y']

        return x_pos + y_pos * self.params['y']

    def get_tile_coords(self, tile):
        x = tile % self.params['y']
        y = tile // self.params['y']
        x_pos = self.params['x0'] + x * self.params['w']
        y_pos = self.params['y0'] + y * self.params['w']
        assert 0 <= x_pos < self.params['x'] * self.params['w']
        assert 0 <= y_pos < self.params['y'] * self.params['w']

        return x_pos, y_pos

    def send_tile_update(self, tile_key):
        x0, y0 = self.get_tile_coords(tile_key)
        data = self.data[x0:x0 + self.params['w'], y0:y0 + self.params['w']]
        self.data_manager.send_tile_update(self, tile_key,
                                           self.serialize(data))

    def send_updates(self, new_data):
        diff = new_data - self.data
        tiles = set()
        diff = np.absolute(diff).sum(-1)
        I, J = diff.shape
        for i in range(I):
            for j in range(J):
                if diff[i, j] != 0:
                    tiles.add(self.get_tile_key(i, j))

        for tile_key in tiles:
            self.send_tile_update(tile_key)

    def parse(self, data):
        return data

    def serialize(self, data):
        return data

    def handle_update(self, tile_key, data):
        x0, y0 = self.get_tile_coords(tile_key)
        self.data[x0:x0 + self.params['w'], y0:y0 + self.params[
            'w']] = self.parse(data)
