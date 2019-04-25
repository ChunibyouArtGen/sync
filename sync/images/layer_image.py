#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import logging
import pickle

import numpy as np

from sync.utils import get_changed_tiles

from .image import Image

logger = logging.getLogger(__name__)

# from .image_registry import image_class


# @image_class("layer")
class LayerImage(Image):
    def __init__(self, data_manager, params):
        super().__init__(data_manager, params)
        self.data = np.full(
            (params["x_count"] * params["w"], params["y_count"] * params["w"], 3),
            254,
            dtype=np.uint8,
        )

    def get_param_list(self):
        return ["layer_name", "x0", "y0", "x_count", "y_count", "w"]

    @classmethod
    def get_type(cls):
        return "layer"

    def get_tile_key(self, x, y):
        x_pos = (x - self.params["x0"]) // self.params["w"]
        y_pos = (y - self.params["y0"]) // self.params["w"]
        try:
            assert 0 <= x_pos < self.params["x_count"]
            assert 0 <= y_pos < self.params["y_count"]
        except Exception as e:
            logger.error("Tile out of bounds, got pos {},{}".format(x_pos, y_pos))
            logger.error(self.params)
            logger.exception(e)

        return x_pos + y_pos * self.params["x_count"]

    def get_tile_coords(self, tile):
        x = tile % self.params["x_count"]
        y = tile // self.params["x_count"]
        x_pos = self.params["x0"] + (x * self.params["w"])
        y_pos = self.params["y0"] + (y * self.params["w"])
        try:
            assert (
                0
                <= x_pos
                < (self.params["x0"] + self.params["x_count"] * self.params["w"])
            )
            assert (
                0
                <= y_pos
                < (self.params["y0"] + self.params["y_count"] * self.params["w"])
            )
        except Exception as e:
            logger.error(
                "Tile {} out of bounds, got coords {},{}".format(tile, x_pos, y_pos)
            )
            logger.error(self.params)
            logger.exception(e)
        return x_pos, y_pos

    async def send_tile_update(self, tile_key):
        x0, y0 = self.get_tile_coords(tile_key)
        x = x0 + self.params["w"]
        y = y0 + self.params["w"]
        data = self.data[x0:x, y0:y, :]

        await self.data_manager.send_tile_update(self, tile_key, data)

    def update_tile_data(self, tile_key, data):
        x0, y0 = self.get_tile_coords(tile_key)
        x = x0 + self.params["w"]
        y = y0 + self.params["w"]
        self.data[x0:x, y0:y, :] = data

    async def update_data(self, new_data):
        logger.debug("Start diff for layer {}...".format(self.params["layer_name"]))

        tiles = get_changed_tiles(self.data, new_data, self.params)

        self.data = new_data
        if len(tiles) != 0:
            logger.info(
                "Detected {} changed tiles in layer {}. Sending updates...".format(
                    len(tiles), self.params["layer_name"]
                )
            )
        for tile_key in tiles:
            asyncio.ensure_future(self.send_tile_update(tile_key))

        return len(tiles) > 0

    def get_image(self):
        return self.data
