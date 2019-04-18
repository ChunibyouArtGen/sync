#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from .Image import Image
import asyncio
import logging
import pickle
logger = logging.getLogger(__name__)

# from .image_registry import image_class


# @image_class("layer")
class LayerImage(Image):
    def __init__(self, data_manager, params):
        super().__init__(data_manager, params)
        self.data = np.zeros((3, params['x_count'] * params['w'],
                              params['y_count'] * params['w']), dtype=np.uint8)

    def get_param_list(self):
        return [
            "layer_name",
            "x0",
            "y0",
            "x_count",
            "y_count",
            "w",
        ]

    @classmethod
    def get_type(cls):
        return 'layer'

    def get_tile_key(self, x, y):
        x_pos = (x - self.params['x0']) // self.params['w']
        y_pos = (y - self.params['y0']) // self.params['w']
        try:
            assert 0 <= x_pos < self.params['x_count']
            assert 0 <= y_pos < self.params['y_count']
        except Exception as e:
            logger.error("Tile {} out of bounds, got pos {},{}".format(tile, x_pos, y_pos))
            logger.error(self.params)
            logger.exception(e)

        return x_pos + y_pos * self.params['y_count']

    def get_tile_coords(self, tile):
        x = tile % self.params['y_count']
        y = tile // self.params['y_count']
        x_pos = self.params['x0'] + x * self.params['w']
        y_pos = self.params['y0'] + y * self.params['w']
        try:
            assert 0 <= x_pos < (self.params['x0'] + self.params['x_count'] * self.params['w'])
            assert 0 <= y_pos < (self.params['y0'] + self.params['y_count'] * self.params['w'])
        except Exception as e:
            logger.error("Tile {} out of bounds, got coords {},{}".format(tile, x_pos, y_pos))
            logger.error(self.params)
            logger.exception(e)
        return x_pos, y_pos

    def send_tile_update(self, tile_key):
        x0, y0 = self.get_tile_coords(tile_key)
        data = self.data[:, x0:(x0 + self.params['w']), y0:(
            y0 + self.params['w'])]
        asyncio.ensure_future(
            self.data_manager.send_tile_update(self, tile_key,
                                               self.serialize_tile_data(data)))
    
    def update_tile_data(self, tile_key, data):
        x0, y0 = self.get_tile_coords(tile_key)
        self.data[:, x0:(x0 + self.params['w']), y0:(
            y0 + self.params['w'])] = self.parse_tile_data(data)

    def update_data(self, new_data):
        diff = new_data - self.data
        tiles = set()
        diff = np.absolute(diff).sum(0)
        I, J = diff.shape
        for i in range(I):
            for j in range(J):
                if diff[i][j] != 0:
                    tiles.add(
                        self.get_tile_key(i + self.params['x0'],
                                          j + self.params['y0']))
        logger.info("Detected {} changed tiles. Sending updates...".format(
            len(tiles)))
        for tile_key in tiles:
            self.send_tile_update(tile_key)

        self.data = new_data

        return len(tiles) > 0

    def parse_tile_data(self, data):
        return pickle.loads(data).copy()

    def serialize_tile_data(self, data):
        return pickle.dumps(data)

    def handle_update(self, tile_key, data):
        x0, y0 = self.get_tile_coords(tile_key)
        self.data[x0:x0 + self.params['w'], y0:y0 +
                  self.params['w']] = self.parse_tile_data(data)

    def get_image(self):
        return self.data