#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import json
import logging
import random
from abc import abstractmethod

from .channel import Channel, handler, handler_functions
from .images import image_classes

logger = logging.getLogger(__name__)


class DataManager:
    def __init__(self, ws):
        self.images = {}
        self.reverse = {}
        self.channel = Channel(ws, self)
        self.dependencies = {}

    def get_new_uuid(self):
        n = random.randrange(10000)
        while n in self.images:
            n = random.randrange(10000)
        logger.debug("Issued id {} for new image".format(n))
        return str(n)

    async def register_image(self, image, uuid=None, update_remote=True):
        if uuid is None:
            uuid = self.get_new_uuid()
        logger.info("Registering new image with uuid {}".format(uuid))
        self.images[uuid] = image
        self.reverse[image] = uuid
        if update_remote:
            logger.info("Sending to remote...")
            asyncio.ensure_future(self.send_image(image))
        else:
            logger.warning("Not informing remote!")
        return uuid

    async def send_image(self, image):
        image_dict = {
            "params": image.get_params(),
            "uuid": self.reverse[image],
            "type": image.get_type(),
        }
        logger.info("Updating remote about new image {}...".format(image_dict))
        await self.channel.send_message("RegisterImage", image_dict)

    async def send_image_definition(self, image_dict):
        logger.info("Updating remote about new image {}...".format(image_dict))
        await self.channel.send_message("RegisterImage", image_dict)

    ## Channel interface funcions

    @handler("RegisterImage")
    async def recv_image_definition(self, image_dict):
        logger.info("Recieved remote image...")
        # logger.debug(json.dumps(image_dict))
        if image_dict["uuid"] in self.images:
            logger.warn("Image already exists (or uuid collision)...")
            return

        # image_dict["data_manager"] = self  # inject the data manager
        Cls = image_classes[image_dict["type"]]
        image = Cls(self, image_dict["params"])
        uuid = image_dict["uuid"]
        self.images[uuid] = image
        self.reverse[image] = uuid
        self.dependencies[image] = []

        # await self.register_image(image, uuid=image_dict["uuid"],update_remote=False)
        logger.info("Loaded image {} successfully".format(image_dict["uuid"]))

    async def send_tile_update(self, image, key, tile_data):
        logger.info("Sending tile update...")
        uuid = self.reverse[image]
        # logger.debug("Handling local tile {} update in image {}...".format(key, uuid))
        message_data = {"uuid": uuid, "tile_key": key, "tile_data": tile_data}

        await self.channel.send_message("UpdateTileData", message_data)

    @handler("UpdateTileData")
    async def recv_tile_update(self, data):
        logger.debug(
            "Updating tile {} in image {}".format(data["tile_key"], data["uuid"])
        )
        image = self.images[data["uuid"]]
        image.update_tile_data(data["tile_key"], data["tile_data"])

    async def send_recompute(self, image):
        logger.info("Sending recompute command...")
        uuid = self.reverse[image]
        message_data = {"uuid": uuid}

        await self.channel.send_message("Recompute", message_data)

    @abstractmethod
    @handler("Recompute")
    async def recv_recompute(self, uuid):
        logger.debug("Scheduling recompute for {}".format(uuid))
        logger.error("Unimplemented!")
