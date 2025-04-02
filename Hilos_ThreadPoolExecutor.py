'''
Created on 1 abr 2025

@author: yo

FORMA FACIL DE INICIAR UN GRUPO DE HILOS

La forma más sencilla de crearlo es como administrador de contexto, 
utilizando la withdeclaración para administrar la creación y destrucción del grupo.


'''

import concurrent.futures
import logging
import threading
import time
def thread_function(name):
    logging.info("Thread %s: iniciando", name)
    time.sleep(2)
    logging.info("Thread %s: terminado", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    for index in range(3):
        logging.info("Main    : creando y iniciando el hilo> %d.", index)
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, range(3))