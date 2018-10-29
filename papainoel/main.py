import random
import time

from threading import Thread, Event, Semaphore

n_renas = 9
n_elfos = 10

# eventos que deixarao renas, elfos e noel esperando
despertador_noel = Event()
despertador_rena = Event()
despertador_elfo = Event()

# semaforo para incremento e decremento de renas e elfos
semaforo = Semaphore()

count_rena = 0
count_elfo = 0

# fila de renas e elfos que foram executados
fila_rena = []
fila_elfo = []


def noel():
    while True:
        if len(fila_rena) == 9:
            print("Papai noel lacou as renas " + str(fila_rena))
            despertador_rena.set()
            fila_rena.clear()
            count_rena = 0
        elif len(fila_elfo) == 3:
            print("Papai noel reuniu com os elfos " + str(fila_elfo))
            despertador_elfo.set()
            fila_elfo.clear()
            count_elfo = 0

        print("Papai noel dormindo.")
        despertador_noel.clear()
        despertador_noel.wait()
        print("Papai noel acordado.")


def rena(id):
    global count_rena
    while True:
        time.sleep(random.random() * 3)
        semaforo.acquire()

        print("Rena: " + str(id))
        if count_rena == 8:
            print("9 renas")
            fila_rena.append(id)
            despertador_noel.set()
            count_rena = 0
        else:
            count_rena += 1
            fila_rena.append(id)

        semaforo.release()
        despertador_rena.clear()
        despertador_rena.wait()
        print('Rena ' + str(id) + ' esta de ferias')


def elfo(id):
    global count_elfo
    while True:
        time.sleep(random.random() * 3)
        semaforo.acquire()

        print("Elfo: " + str(id))
        if count_elfo == 2:
            if len(fila_rena) < 9:
                fila_elfo.append(id)
                print("3 elfos")
                despertador_noel.set()
                count_elfo = 0
        else:
            count_elfo += 1
            fila_elfo.append(id)

        semaforo.release()
        despertador_elfo.clear()
        despertador_elfo.wait()
        print('Elfo ' + str(id) + ' foi fazer brinquedo')


if __name__ == "__main__":
    # criando e comecando a thread papei noel
    noel = Thread(target=noel)
    noel.start()

    # criando e comecando as threads (renas)
    renas = []
    for r in range(n_renas):
        renas.append(Thread(target=rena, args=(r,)))

    for r in range(n_renas):
        renas[r].start()

    # criando e comecando as threads (elfos)
    elfos = []
    for e in range(n_elfos):
        elfos.append(Thread(target=elfo, args=(e,)))

    for e in range(n_elfos):
        elfos[e].start()
