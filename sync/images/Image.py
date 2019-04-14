#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod, abstractclassmethod


class Image(ABC):
    @abstractmethod
    def __init__(self, data_manager, params):
        """
        This method stores the data manager and parameters as internal variables.
        This method also handles validates the passed params, to ensure they contain 
        all the necessary parameters (i.e what get_param_list returns).

        Build on top of this in subclasses. 
        """
        self.data = None
        self.data_manager = data_manager

        for param in self.get_param_list():
            assert param in params

        self.params = params

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