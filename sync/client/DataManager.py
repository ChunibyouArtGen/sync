import asyncio
import logging

from sync.data_manager import DataManager

logger = logging.getLogger(__name__)


class ClientDataManager(DataManager):
    async def watch_layers(self):
        while True:
            logger.debug("Scanning layer images...")
            for uuid, image in self.images.items():
                await image.scan()

                state = image.krita_node.visible()
                image.krita_node.setVisible(not state)
                image.krita_node.setVisible(state)
                image.krita_node.setVisible(not state)
                image.krita_node.setVisible(state)

            await asyncio.sleep(1)

    async def recv_recompute(self, uuid):
        logger.debug("Scheduling recompute for {}".format(uuid))

    async def recv_tile_update(self, data):
        logger.debug(
            "Updating tile {} in image {}".format(data["tile_key"], data["uuid"])
        )
        image = self.images[data["uuid"]]
        image.update_tile_data(data["tile_key"], data["tile_data"])

    async def register_image(self, image, *args):
        uuid = await super().register_image(image, *args)
        asyncio.ensure_future(image.scan())
        return uuid
