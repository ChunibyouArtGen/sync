import asyncio
import logging

import websockets

from sync import init_logging

from .DataManager import ServerDataManager

logger = logging.getLogger()


class Server:
    def __init__(self, log_level=logging.INFO):
        init_logging(level=log_level)
        self.data_manager = None

    async def handle_message(self, ws, path):
        try:
            logger.info("Running handler...")
            if self.data_manager is None:
                self.data_manager = ServerDataManager(ws)
                logger.info("Server init complete")

            while True:
                logger.info("Waiting for message...")
                message = await ws.recv()
                logger.info("Got message!")
                await self.data_manager.channel.process_message(message)
        except:
            import sys

            sys.exit()

    def start(self, host="localhost", port=8765):
        start_server = websockets.serve(self.handle_message, host, port)
        logger.info("Starting server...")
        try:
            loop = asyncio.gather(start_server)
        except:
            logger.warning("Quitting!")
            return
        asyncio.get_event_loop().run_until_complete(loop)
        asyncio.get_event_loop().run_forever()
