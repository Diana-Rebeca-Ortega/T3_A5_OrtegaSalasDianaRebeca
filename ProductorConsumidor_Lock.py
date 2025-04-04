import random
import logging
import threading
import time
import concurrent.futures
import queue

SENTINEL = object()

class Pipeline:
    def __init__(self):
        self.queue = queue.Queue()
        self.sender = None
        self.receiver = None

    def set_message(self, message, sender):
        self.sender = sender
        self.queue.put(message)

    def get_message(self, receiver):
        self.receiver = receiver
        return self.queue.get()

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
        
        
        
