#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod, abstractclassmethod
import logging
logger = logging.getLogger(__name__)


class Image(ABC):
    def __init__(self, data_manager, params):
        self.params = params
        self.data = None
        self.data_manager = data_manager
        data_manager.register_image(self)

        for param in self.get_param_list():
            try:
                assert param in params
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
    def handle_update(self, tile_key, data):
        pass

    @abstractmethod
    def get_image(self):
        pass

    @abstractmethod
    def scan(self):
        """
        Update the image. Typically called by the DataManager or TaskRunner.
        """
        pass

    @abstractclassmethod
    def get_type(cls):
        pass

    def get_params(self):
        return self.params