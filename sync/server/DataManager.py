from sync.data_manager import DataManager
import logging
import asyncio
from .compute import TaskManager
from .ServerComputedImage import ServerComputedImage
from .ServerLayerImage import ServerLayerImage

logger = logging.getLogger(__name__)


class ServerDataManager(DataManager):
    def __init__(self, ws):
        super().__init__(ws)
        self.taskmanager = TaskManager(self)
        self.dependencies = {}
        logger.info("Data Manager initialized successfully")

    async def recv_recompute(self, uuid):
        logger.debug("Scheduling recompute for {}".format(uuid))
        image = self.images[uuid]
        self.taskmanager.compute_debounce(image)

    def add_dependency(self, source, dependent):
        if source not in self.dependencies:
            self.dependencies[source] = []
        self.dependencies[source].append(dependent)

    def recompute_dependencies(self, source):
        for dependency in self.dependencies[source]:
            asyncio.ensure_future(self.taskmanager.compute_debounce(dependency))

    async def recv_tile_update(self, data):
        logger.info(
            "Updating tile {} in image {}".format(data["tile_key"], data["uuid"])
        )
        image = self.images[data["uuid"]]
        image.update_tile_data(data["tile_key"], data["tile_data"])
        self.recompute_dependencies(image)
