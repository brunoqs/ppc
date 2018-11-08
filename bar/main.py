import random
import time
import sys

from threading import Thread, Event, Semaphore

despertador_garcon = []
despertador_cliente = Event()

semaforo = Semaphore()

count_cliente = 0
count_rodada = 0
count_loop = 0

fila_cliente = []


def garcon(id):
    ''' Funcao sera executada quando n clientes tiverem feito o pedido '''
    global count_loop
    while True:
        semaforo.acquire()
        if len(fila_cliente) == c_garcon or count_loop == n_clientes:
            print("Garcon " + str(id) + " buscando pedidos " + str(fila_cliente))
            fila_cliente.clear()

        if count_loop == n_clientes:
            count_loop = 0
            despertador_cliente.set()

        print("Garcon " + str(id) + " esperando pedido.")
        semaforo.release()

        despertador_garcon[id].clear()
        despertador_garcon[id].wait()


def cliente(id):
    ''' Funcao sera executada ate que o numero de rodadas seja atingido, quando n clientes (threads) foram criadas
        o garcom (thread) sera chamado aleatoriamente '''
    global count_cliente, count_loop
    while True:
        time.sleep(random.random() * 5)
        semaforo.acquire()
        count_loop += 1
        if random.randint(0, 3) == 2:
            print("Cliente " + str(id) + " nao pediu nada")
        else:
            print("Cliente " + str(id) + ' fez pedido')
            if count_cliente == c_garcon - 1 or count_loop == n_clientes:
                fila_cliente.append(id)
                if count_cliente == c_garcon - 1:
                    print("Numero de clientes do garcom atingido.")
                else:
                    print("Todos os clientes fizeram pedido")

                while True:
                    g = random.randint(0, n_garcons - 1)
                    if not despertador_garcon[g].isSet():
                        despertador_garcon[g].set()
                        break

                count_cliente = 0

            else:
                count_cliente += 1
                fila_cliente.append(id)
        semaforo.release()

        despertador_cliente.clear()
        despertador_cliente.wait()
        print('Cliente ' + str(id) + ' esta consumindo.')
        time.sleep(random.random() * 2)


if __name__ == "__main__":
    if len(sys.argv) <= 4:
        print("Informe o numero de clientes, número de garçons, capacidade dos garçons e número de rodadas.")
        sys.exit()

    n_clientes = int(sys.argv[1])
    n_garcons = int(sys.argv[2])
    c_garcon = int(sys.argv[3])
    qt_rodada = int(sys.argv[4])

    # criando e comecando as threads garcons
    garcons = []
    for g in range(n_garcons):
        garcons.append(Thread(target=garcon, args=(g,)))
        despertador_garcon.append(Event())

    for g in range(n_garcons):
        garcons[g].start()

    # criando e comecando as threads clients
    clientes = []
    for c in range(n_clientes):
        clientes.append(Thread(target=cliente, args=(c,)))

    for c in range(n_clientes):
        clientes[c].start()
