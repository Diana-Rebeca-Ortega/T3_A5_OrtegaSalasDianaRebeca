'''
Created on 1 abr 2025

@author: Yo
'''
import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: iniciado...", name)
    time.sleep(2)
    logging.info("Thread %s: terminado...", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : antes de crear hilo")
    ##CREACION DEL HILO, Se agrego el demonio
    x = threading.Thread(target=thread_function, args=(1,), daemon=True)
    logging.info("Main    : antes de ejecutar el hilo")
    ##INICIO DEL HILO
    x.start()
    
    ## join> > >Para indicar a un hilo que espere a que otro termine
    #Si se descomenta esa línea, el hilo principal se pausará y esperará a que el hilo xtermine de ejecutarse
    logging.info("Main    : Espera a que termine el hilo")
    x.join()
    logging.info("Main    : todo hecho")
    
    
    