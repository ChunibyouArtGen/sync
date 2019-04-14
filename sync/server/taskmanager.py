import logging
from concurrent.futures import ThreadPoolExecutor
from .models import NSTModel
logger = logging.getLogger(__name__)



class TaskManager:
    def __init__(self):
        self.models = {'nst': NSTModel()}
        self.executor = ThreadPoolExecutor()

    def compute(self, image, slots):
        logger.info('Computing...')
        model_id = image.params['model_id']
        inputs = {slot: image.get_data() for slot,image in slots.items()}
        image_data = self.models['model_id'].run(inputs)
        logger.info('Done! Informing Image object...')
        image.recv_computed_image(image_data)
    
    def schedule_compute(self, image, slots):
        self.executor.submit(self.compute, image, slots)