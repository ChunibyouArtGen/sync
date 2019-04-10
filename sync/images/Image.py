#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod,abstractclassmethod
import logging
logger = logging.getLogger(__name__)

class Image(ABC):
    @abstractmethod
    def __init__(self, data_manager, params):
        self.data = None
        self.data_manager = data_manager
        
        for param in self.get_param_list():
            try:
                assert param in params
            except:
                logger.critical("Missing param {} for type {}".format(param, self.get_type()))
                raise        

        self.params = params

    @abstractmethod
    def get_param_list(self):
        return []

    @abstractmethod
    def handle_update(self, tile_key, data):
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