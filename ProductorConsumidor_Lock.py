import random
import logging
import threading
import time
import concurrent.futures
import queue

SENTINEL = object()

class Pipeline:
    """
    Class to allow a single element pipeline between producer and consumer.
    """
    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()

    def get_message(self, name):
        logging.debug("%s:A punto de adquirir getlock", name)
        self.consumer_lock.acquire()
        logging.debug("%s:tener bloqueo", name)
        message = self.message
        logging.debug("%s:A punto de liberar el bloqueo", name)
        self.producer_lock.release()
        logging.debug("%s:bloqueo liberado", name)
        return message

    def set_message(self, message, name):
        logging.debug("%s:a punto de adquirir setlock", name)
        self.producer_lock.acquire()
        logging.debug("%s:tener setlock", name)
        self.message = message
        logging.debug("%s:A punto de liberar getlock", name)
        self.consumer_lock.release()
        logging.debug("%s:obtener bloqueo liberado", name)

def producer(pipeline):
    """Imagina que recibimos un mensaje de la red."""
    for index in range(10):
        message = random.randint(1, 101)
        logging.info("El productor recibió un mensaje: %s", message)
        pipeline.set_message(message, "Producer")
    # Envíe un mensaje centinela para avisarle al consumidor que hemos terminado
    pipeline.set_message(SENTINEL, "Producer")

def consumer(pipeline):
    """Pretend we're saving a number in the database."""
    while True:
        message = pipeline.get_message("Consumer")
        if message is SENTINEL:
            break
        logging.info("Consumer storing message: %s", message)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)
    pipeline = Pipeline()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(consumer, pipeline)
        executor.submit(producer, pipeline)
        
        
        
