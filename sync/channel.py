import json as bson
import logging

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
        await self.ws.send(bson.dumps(message))

    async def process_message(self, message):
        r = bson.loads(message)
        logger.info("Got message {}".format(r))
        request = r['request']
        data = r["data"]
        if request == "RegisterImage":
            await self.data_manager.recv_image_definition(data)
        elif request == "UpdateTileData":
            await self.data_manager.recv_tile_update(data)
        # elif message["request"] == "RegisterImage":
        #    self.data_manager.update_tile()

    async def listen(self):
        logger.info("Listening for updates...")
        while True:
            message = await self.ws.recv()
            logger.info("Got a message!")
            await self.process_message(message)
