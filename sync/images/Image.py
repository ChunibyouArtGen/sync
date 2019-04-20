#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod, abstractclassmethod
import logging
logger = logging.getLogger(__name__)
import asyncio


class Image(ABC):
    def __init__(self, data_manager, params):
        self.params = params
        self.data = None
        self.data_manager = data_manager
        
        for param in self.get_param_list():
            try:
                assert param in params
                try:
                    self.params[param] = int(params[param])
                except:
                    try:
                        self.params[param] = float(params[param])
                    except:
                        pass
            except:
                logger.critical("Missing param {} for type {}".format(
                    param, self.get_type()))
                raise

    @abstractmethod
    def get_param_list(self):
        """
        Returns a list of expected parameters. This list is used:
        1. During initialization of the object, to validate that parameters are present.
        2. As a layout for generating a serialized representation for storage or transfer over
        the network.
        """
        return []

    
    @abstractmethod
    def get_image(self):
        pass

    @abstractclassmethod
    def get_type(cls):
        pass

    def get_params(self):
        return self.params

    async def register_self(self):
        await self.data_manager.register_image(self)