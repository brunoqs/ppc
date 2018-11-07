import random
import time
import sys

from threading import Thread, Event, Semaphore

n_clientes = int(sys.argv[1])
n_garcons = int(sys.argv[2])
c_garcon = int(sys.argv[3])
qt_rodada = int(sys.argv[4])

# eventos que deixarao renas, elfos e noel esperando
despertador_garcon = []
despertador_cliente = []

# semaforo para incremento de renas e elfos
semaforo = Semaphore()

count_cliente = 0
count_rodada = 0
count_loop = 0

# fila de renas e elfos que foram executados
fila_cliente = []

def garcon(id):
    ''' Funcao sera executada quando n clientes tiverem feito o pedido '''
    while True:
        if count_loop == n_clientes * qt_rodada:
            print("Bar fechou")
            break

        semaforo.acquire()
        if len(fila_cliente) == c_garcon or len(fila_cliente) == n_clientes:
            print("Garcon " + str(id) + " buscando pedidos " + str(fila_cliente))
            for i in fila_cliente:
                despertador_cliente[i].set()
            fila_cliente.clear()

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
        if count_loop == n_clientes * qt_rodada:
            print("Bar fechou")
            break

        if random.randint(0, 3) == 2:
            print("Cliente " + str(id) + " nao pediu nada")
        else:
            semaforo.acquire()
            print("Cliente " + str(id) + ' fez pedido')
            if count_cliente == c_garcon - 1 or count_cliente + 1 == n_clientes:
                fila_cliente.append(id)
                if count_cliente == c_garcon - 1:
                    print("Numero de clientes do garcom atingido.")
                else:
                    print("Todos os clientes fizeram pedido")

                while True:
                    g = random.randint(0, n_garcons-1)
                    if not despertador_garcon[g].isSet():
                        despertador_garcon[g].set()
                        break

                count_cliente = 0
            
            else:
                count_cliente += 1
                fila_cliente.append(id)

        count_loop += 1
        semaforo.release()

        despertador_cliente[id].clear()
        despertador_cliente[id].wait()
        print('Cliente ' + str(id) + ' esta consumindo.')
        time.sleep(random.random() * 2)


if __name__ == "__main__":
    if len(sys.argv) <= 4:
        print("Informe o numero de anos")
        sys.exit()

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
        despertador_cliente.append(Event())

    for c in range(n_clientes):
        clientes[c].start()
