from sync.data_manager import DataManager
import logging
import asyncio
logger = logging.getLogger(__name__)


class ClientDataManager(DataManager):
    async def watch_layers(self):
        while True:
            logger.debug("Scanning layer images...")
            for uuid, image in self.images.items():
                await image.scan()
                
            await asyncio.sleep(5)

    async def recv_recompute(self, uuid):
        logger.debug("Scheduling recompute for {}".format(uuid))
        
    async def recv_tile_update(self, data):
        logger.info("Updating tile {} in image {}".format(data['tile_key'], data['uuid']))
        image = self.images[data['uuid']]
        image.update_tile_data(data['tile_key'], data['tile_data'])
        