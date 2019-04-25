import websockets
import asyncio
from .ClientComputedImage import ClientComputedImage
from .ClientLayerImage import ClientLayerImage
from .DataManager import ClientDataManager
import logging
from threading import Thread

logger = logging.getLogger(__name__)

client_obj = None


def get_client(host='localhost', port='8765', reset=False):
    global client_obj
    if not client_obj or reset == True:
        client_obj = Client()
        client_obj.start_thread()
    return client_obj


class Client:
    def __init__(self):
        self.asyncio_loop = None

    def get_data_manager(self):
        return self.data_manager

    async def connect(self, host, port):
        ws = await websockets.connect('ws://{}:{}'.format(host, port))
        self.data_manager = ClientDataManager(ws)
        logger.info("Client init complete")
        await asyncio.gather(self.data_manager.channel.listen(),
                             self.data_manager.watch_layers())

    def start_thread(self):
        t = Thread(target=self.start, args=['localhost','8765'], name='celestiaprime')
        t.start()

    def run_coroutine(self, cor):
        asyncio.run_coroutine_threadsafe(cor, loop=self.asyncio_loop)

    async def run(self, host, port):
        logger.info("Worker thread started")
        await self.connect(host, port)

    def start(self, host, port):
        self.asyncio_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.asyncio_loop)
        asyncio.ensure_future(self.run(host,port))
        asyncio.get_event_loop().run_forever()
