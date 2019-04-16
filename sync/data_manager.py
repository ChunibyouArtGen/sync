#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import logging
import random
import json
from .channel import Channel, handler_functions, handler
from .images import image_classes
from abc import abstractmethod
import asyncio

logger = logging.getLogger(__name__)


class DataManager:
    def __init__(self, ws):
        self.images = {}
        self.reverse = {}
        self.dependencies = {}
        self.channel = Channel(ws, self)
        
    def get_new_uuid(self):
        n = random.randrange(10000)
        while n in self.images:
            n = random.randrange(10000)
        logger.debug("Issued id {} for new image".format(n))
        return str(n)

    def add_dependency(self, source, dependent):
        if source not in self.dependencies:
            self.dependencies[source] = []
        self.dependencies[source].append(dependent)


    def recompute_dependencies(self, source):
        for dependency in self.dependencies[source]:
            self.send_recompute(dependency)



    async def register_image(self, image, uuid=None, update_remote=True):
        if uuid is None:
            uuid = self.get_new_uuid()
        logger.info("Registering new image with uuid {}".format(uuid))
        self.images[uuid] = image
        self.reverse[image] = uuid
        self.dependencies[image] = []
        if update_remote:
            logger.info("Sending to remote...")
            await self.send_image(image)
        else:
            logger.warning("Not informing remote!")
        return uuid

    async def send_image(self, image):
        image_dict = {
            'params': image.get_params(),
            "uuid": self.reverse[image],
            'type': image.get_type()
        }
        logger.info("Updating remote about new image {}...".format(image_dict))
        await self.channel.send_message("RegisterImage", image_dict)


    async def send_image_definition(self, image_dict):
        logger.info("Updating remote about new image {}...".format(image_dict))
        await self.channel.send_message("RegisterImage", image_dict)

    
    ## Channel interface funcions
    
    @handler("RegisterImage")
    async def recv_image_definition(self, image_dict):
        print(image_classes)
        logger.info("Recieved remote image...")
        #logger.debug(json.dumps(image_dict))
        if image_dict["uuid"] in self.images:
            logger.warn("Image already exists (or uuid collision)...")
            return

        image_dict["data_manager"] = self  # inject the data manager
        Cls = image_classes[image_dict['type']]
        image = Cls(self, image_dict['params'])

        await self.register_image(image, uuid=image_dict["uuid"],update_remote=False)
        logger.info("Loaded image {} successfully".format(image_dict['uuid']))


    async def send_tile_update(self, image, key, tile_data):
        logger.info("Sending tile update...")
        uuid = self.reverse[image]
        #logger.debug("Handling local tile {} update in image {}...".format(key, uuid))
        message_data = {"uuid": uuid, "tile_key": key, "tile_data": tile_data}

        await self.channel.send_message("UpdateTileData", message_data)

    @handler("UpdateTileData")
    async def recv_tile_update(self, data):
        logger.debug("Updating tile {} in image {}".format(data['tile_key'], data['uuid']))
        image = self.reverse[data['uuid']]
        image.update_tile_data(data['tile_key'], data['tile_data'])


    async def send_recompute(self, image):
        logger.info("Sending recompute command...")
        uuid = self.reverse[image]
        message_data = {"uuid": uuid}

        await self.channel.send_message("Recompute", message_data)

    @abstractmethod
    @handler("Recompute")
    async def recv_recompute(self, uuid):
        logger.debug("Scheduling recompute for {}".format(uuid))
        

    ## Control functions
    @abstractmethod
    async def watch_layers(self):
        pass
        while True:
            logger.debug("Scanning layer images...")
            for _, image in self.images.items():
                image.update()
                    

            await asyncio.sleep(2)
