import logging
import threading
import time
import concurrent.futures
import random

class Pipeline:
    """
    Clase que permite una canalización de un único elemento entre el productor y el consumidor.
    """
    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()

    def get_message(self, name):
        self.consumer_lock.acquire()
        message = self.message
        self.producer_lock.release()
        return message

    def set_message(self, message, name):
        self.producer_lock.acquire()
        self.message = message
        self.consumer_lock.release()
        


SENTINEL = object()

def producer(pipeline):
    """Imagina que recibimos un mensaje de la red.."""
    for index in range(10):
        message = random.randint(1, 101)
        logging.info("El productor recibió un mensaje.e: %s", message)
        pipeline.set_message(message, "Producer")

    #Envíe un mensaje centinela para avisarle al consumidor que hemos terminado
    pipeline.set_message(SENTINEL, "Producer")        
        
        
def consumer(pipeline):
    """Imagina que estamos guardando un número en la base de datos.."""
    message = 0
    while message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info("Mensaje de almacenamiento del consumidor: %s", message)        
        
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Pipeline()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)        
    