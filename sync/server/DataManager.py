from sync.data_manager import DataManager
import logging
import asyncio
from .taskmanager import TaskManager
from .ServerComputedImage import ServerComputedImage
from .ServerLayerImage import ServerLayerImage

logger = logging.getLogger(__name__)


class ServerDataManager(DataManager):
    def __init__(self, ws):
        super().__init__(ws)
        self.taskmanager = TaskManager()
        logger.info("Data Manager initialized successfully")

    async def recv_recompute(self, uuid):
        logger.debug("Scheduling recompute for {}".format(uuid))
        image = self.images[uuid]
        self.taskmanager.schedule_compute(image, image.slots)