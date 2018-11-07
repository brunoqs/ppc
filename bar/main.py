import random
import time
import sys

from threading import Thread, Event, Semaphore

n_clientes = int(sys.argv[1])
n_garcons = int(sys.argv[2])
c_garcon = int(sys.argv[3])
qt_rodada = int(sys.argv[4])

# eventos que deixarao renas, elfos e noel esperando
despertador_garcon = Event()
despertador_cliente = Event()

# semaforo para incremento de renas e elfos
semaforo = Semaphore()

count_cliente = 0
count_rodada = 0

# fila de renas e elfos que foram executados
fila_cliente = []
fila_garcon = []
count_garcon = []



def garcon(id):
    ''' Funcao sera executada quando 9 threads renas ou 3 threads elfo estiverem prontas,
    ela para de acordo com os anos setados na entrada no programa '''
    global count_cliente
    while True:
        if len(fila_cliente) != 0:
            temp = fila_cliente[-1]
            if not fila_cliente[-1] == -5:
                print("Cliente " + str(temp) + ' fez pedido para o garcon ' + str(id))

                count_garcon.append(id)

                if count_garcon.count(id) == c_garcon:
                    count_garcon.clear()
                    if not fila_cliente[-1] == -5:
                        fila_garcon.append(fila_cliente[-1])
                        fila_cliente[-1] = -5
                    print("Garcon " + str(id) + " buscando pedidos " + str(fila_garcon))
                    
                    
                    despertador_cliente.set()
                    fila_cliente.clear()
                    fila_garcon.clear()
                    count_cliente = 0

                elif not fila_cliente[-1] == -5:
                    fila_garcon.append(fila_cliente[-1])
                    fila_cliente[-1] = -5


        
        else:
            print("Garcon " + str(id) + " esperando pedido.")

        
        despertador_garcon.clear()
        despertador_garcon.wait()

def cliente(id):
    ''' Funcao acorda a thread papai noel quando 3 threads renas estiverem prontas (da prioridade as renas), ela so ira parar
    quando as threds renas ja tiverem parado '''
    global count_cliente
    while True:
        time.sleep(random.random() * 3)

        semaforo.acquire()
        #print("Cliente " + str(id) + ' fez pedido')
        
        fila_cliente.append(id)
        count_cliente += 1
        despertador_garcon.set()
        

        semaforo.release()

        despertador_cliente.clear()
        despertador_cliente.wait()
        print('Cliente ' + str(id) + ' esta bebendo.')
        x = (int) (random.random() * 5) + 1
        time.sleep(x)
        print('Cliente ' + str(id) + ' terminou de beber em ' + str(x) + ' minutos')


if __name__ == "__main__":
    if len(sys.argv) <= 4:
        print("Informe o numero de anos")
        sys.exit()

    # criando e comecando as threads garcons
    garcons = []
    for g in range(n_garcons):
        garcons.append(Thread(target=garcon, args=(g,)))
    
    for g in range(n_garcons):
        garcons[g].start()

    # criando e comecando as threads clients
    clientes = []
    for c in range(n_clientes):
        clientes.append(Thread(target=cliente, args=(c,)))

    for c in range(n_clientes):
        clientes[c].start()
