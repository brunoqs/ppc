import random
import time
import sys

from threading import Thread, Event, Semaphore

import colored.style as s
import colored.fore as f
import colored.back as b

BLINK = "\033[5;30m"


def printt(text, box=False):
    if not box:
        print(text + s.RESET)
    else:
        printbox(text)


def printbox(msg, cbox=s.RESET + f.WHITE, ctext=s.BOLD + f.WHITE):
    row = len(msg) + 2

    x = cbox + '+' + s.RESET
    y = cbox + '-' + s.RESET
    v = cbox + '|' + s.RESET

    msg = ctext + " " + msg + " " + s.RESET

    h = ''.join([x] + [y * row] + [x])
    result = h + '\n' + v + msg + v + '\n' + h
    print("\n" + result + "\n" + s.RESET)


def hohoho():
    print(BLINK + f.RED + " \t" + r"__     _  __ ")
    print(BLINK + f.RED + " \t" + r"| \__ `\O/  `--  {}    \}    {/")
    print(BLINK + f.RED + " \t" + r"\    \_(~)/______/=____/=____/=*")
    print(BLINK + f.RED + " \t" + r" \=======/    //\\  >\/> || \> ")
    print(BLINK + f.RED + " \t" + r"----`---`---  `` `` ```` `` ``")
    print(BLINK + f.RED + " \t" + r" * F E L I Z     N A T A L * *")
    printt("" + s.RESET)


n_renas = 9
n_elfos = 10

anos = n_renas

# eventos que deixarao renas, elfos e noel esperando
despertador_noel = Event()
despertador_rena = Event()
despertador_elfo = Event()

# semaforo para incremento de renas e elfos
semaforo = Semaphore()

count_rena = 0
count_elfo = 0
count_loop = 0

# fila de renas e elfos que foram executados
fila_rena = []
fila_elfo = []


def noel():
    ''' Funcao sera executada quando 9 threads renas ou 3 threads elfo estiverem prontas,
    ela para de acordo com os anos setados na entrada no programa '''
    while True:
        if len(fila_rena) == 9:
            hohoho()
            printt(s.BOLD + f.RED + "Papai noel lançou as renas " + f.WHITE + b.ORANGE_4B + str(
                fila_rena) + b.BLACK + "\n")

            despertador_rena.set()
            fila_rena.clear()
            global count_rena
            count_rena = 0

            if count_loop == anos:
                printt(f.RED + s.BOLD + "-> Papai noel foi dormir zZz")
                despertador_elfo.set()
                break

        elif len(fila_elfo) == 3:
            printt(s.BOLD + f.RED + "Papai noel reuniu com os elfos " + f.WHITE + b.GREEN + str(fila_elfo))
            despertador_elfo.set()
            fila_elfo.clear()
            global count_elfo
            count_elfo = 0

        printt(s.BOLD + f.RED + "-> Papai noel foi dormir zZz")
        despertador_noel.clear()
        despertador_noel.wait()
        printt(s.BOLD + f.RED + "<- Papai noel acordou :D")


def rena(id):
    ''' Funcao acorda a thread papai noel quando 9 threads renas estiverem prontas, ela so ira parar quando
    as 9 threads renas forem executadas de acordo com os anos '''
    global count_rena, count_loop
    while True:
        time.sleep(random.random() * 3)
        if count_loop == anos:
            break

        semaforo.acquire()
        printt(f.ORANGE_4B + s.BOLD + "Rena: [ " + s.RESET + f.ORANGE_4B + str(id) + " ]")
        if count_rena == 8:
            printbox("9 renas!", cbox=BLINK + f.ORANGE_4B)
            fila_rena.append(id)
            despertador_noel.set()
            count_rena = 0
        else:
            count_rena += 1
            fila_rena.append(id)

        count_loop += 1
        semaforo.release()

        despertador_rena.clear()
        despertador_rena.wait()
        printt(s.BOLD + f.ORANGE_4B + 'Rena [ ' + str(id) + ' ] ' + s.RESET + 'está de ferias')


def elfo(id):
    ''' Funcao acorda a thread papai noel quando 3 threads renas estiverem prontas (da prioridade as renas), ela so ira parar
    quando as threds renas ja tiverem parado '''
    global count_elfo
    while True:
        time.sleep(random.random() * 3)
        if count_loop == anos:
            printt(f.GREEN + s.BOLD + 'Elfo ( ' + str(id) + ' ) ' + s.RESET + 'foi fazer brinquedo')
            break

        semaforo.acquire()
        printt(f.GREEN + s.BOLD + "Elfo: " + s.RESET + f.GREEN + str(id))
        if count_elfo == 2:
            if len(fila_rena) < 9:
                fila_elfo.append(id)
                printbox("3 elfos!", cbox=BLINK + f.GREEN)
                despertador_noel.set()
                count_elfo = 0
        else:
            count_elfo += 1
            fila_elfo.append(id)

        semaforo.release()

        despertador_elfo.clear()
        despertador_elfo.wait()

        printt(f.GREEN + s.BOLD + 'Elfo ( ' + str(id) + ' ) ' + s.RESET + 'foi fazer brinquedo')


if __name__ == "__main__":

    if len(sys.argv) <= 1:
        printt("Informe o numero de anos:")
        sys.exit()

    anos = anos * int(sys.argv[1])

    # criando e comecando a thread papai noel
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
