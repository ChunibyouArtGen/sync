import logging
from concurrent.futures import ThreadPoolExecutor
from .models import NSTModel
logger = logging.getLogger(__name__)



class TaskManager:
    def __init__(self, data_manager):
        self.models = {'nst': NSTModel()}
        self.executor = ThreadPoolExecutor()
        self.data_manager = data_manager

    def compute(self, image, input_slots):
        logger.info('Computing...')
        model_id = image.params['model_id']
        inputs = {}
        for slot, image in input_slots:
            try:
                inputs[slot] = image.get_data()
            except:
                inputs[slot] = image
        
        image_data = self.models[model_id].run(inputs)
        logger.info('Done! Informing Image object...')
        image.recv_computed_image(image_data)
    
    def schedule_compute(self, image, slots):
        self.executor.submit(self.compute, image, slots)
    
    def listen(self, data_manager):
        pass