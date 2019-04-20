import logging
from concurrent.futures import ThreadPoolExecutor, Future
from .models import NSTModel
import asyncio
logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self, data_manager):
        self.models = {'nst': NSTModel()}
        self.executor = ThreadPoolExecutor()
        self.data_manager = data_manager
        self.tasks = {}
        self.loop = asyncio.get_event_loop()

    def compute(self, image):
        logger.info('Computing...')
        model_id = image.params['model_id']
        inputs = {}
        input_slots = image.get_slots()

        for slot, image in input_slots:
            try:
                inputs[slot] = image.get_data()
            except:
                inputs[slot] = image

        image_data = self.models[model_id].run(inputs)
        logger.info('Done!')
        return image_data
        #image.update_data(image_data)
        
    async def schedule_compute(self, image):
        logger.info('Sending compute request to executor')
        future = self.executor.submit(self.compute, args=[image])

        def callback(future:Future):
            data = future.result()
            logger.info("Handling computed data...")
            image.update_data(data)
        
        future.add_done_callback(callback)

    
    async def compute_debounce(self, image):
        try:
            
            if self.tasks[image]:
                status = self.tasks[image].cancel() # Cancel other executions of this function
                if status == False:
                    logger.warn('Computation cancel failed. The task is (probably) already running.')

            await asyncio.sleep(5)  # Give other executions a chance to cancel this this one
            
            self.tasks[image] = asyncio.ensure_future(self.schedule_compute(image)) # Defer to the actual function

        except:
            logger.warn('Compute scheduling aborted')
            raise



    def listen(self, data_manager):
        pass