#import bson
import logging
import pickle
logging.getLogger('bson').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

handler_functions = {}

def handler(messagetype):
    def decorator(f):
        handler_functions[messagetype] = f
        return f
    return decorator

class Channel:
    def __init__(self, ws, data_manager):
        self.ws = ws
        self.data_manager = data_manager
        self.handlers = {}


    async def send_message(self, request, data):
        logger.info("Sending message {}".format(request))
        message = {"request": request, "data": data}
        data = pickle.dumps(message)
        #data = bson.dumps(message)
        await self.ws.send(data)

    async def process_message(self, message):
        #r = bson.loads(message)
        r = pickle.loads(message)
        logger.info("Got message {}".format(r['request']))
        request = r['request']
        data = r["data"]
        if request == "RegisterImage":
            await self.data_manager.recv_image_definition(data)
        elif request == "UpdateTileData":
            await self.data_manager.recv_tile_update(data)
        
    async def listen(self):
        logger.info("Listening for updates...")
        while True:
            message = await self.ws.recv()
            logger.info("Got a message!")
            await self.process_message(message)
