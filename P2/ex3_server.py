import argparse
import socket
import numpy as np

#Funcion que comprueba si acierta el tiro
def comprobar_barco(tablero_rival,fila,columna):
    if(tablero_rival[fila,columna] == 1):       #Se comprueba si la posición elegida por un jugador es un barco en el tablero rival
        return True
    else:
        return False

#Funcion que comprueba si hay navios restantes
def hay_navios(tablero_rival):
    awnser = False
    for f in range(10):
        for c in range(10):             #Se recorre la matriz 10x10, el momento que se encuentre un barco awnser se pone True y se devuelve\
            if tablero_rival[f,c]==1:     #sino el juego tiene que finalizar
                awnser = True
                return awnser

    return awnser

def main(host, port):
    buffersize = 1024
    #Creamos y enlazamos el socket
    ServerSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    ServerSocket.bind((host, port))

    print("[Starting] Server UP and waiting players.")

    BytesJ1,addr_J1 = ServerSocket.recvfrom(buffersize)         #Leemos y decodificamos el nombre y el tablero del Jug 1
    N_J1 = BytesJ1.decode("utf-8")
    print(N_J1+" has joined the game (Address: "+ str(addr_J1) + " )") 

    BytesJ1,addr_J1 = ServerSocket.recvfrom(buffersize)
    tablero_J1 = BytesJ1.decode("utf-8")
    print(N_J1+"'s Board has been recieved.")

    BytesJ2,addr_J2 = ServerSocket.recvfrom(buffersize)         #Leemos y decodificamos el nombre y el tablero del Jug 2
    N_J2 = BytesJ2.decode("utf-8")
    print(N_J2+" has joined the game (Address: "+ str(addr_J2) + " )")

    BytesJ2, addr_J2 = ServerSocket.recvfrom(buffersize)
    tablero_J2 = BytesJ2.decode("utf-8")
    print(N_J2+"'s Board has been recieved.")

    #----DATOS RECIBIDOS----#

    tablero_J1 = np.matrix(tablero_J1,int)      #Formamos las matrices de los tableros (string a matriz de enteros)
    tablero_J2 = np.matrix(tablero_J2, int)

    #Inicializamos los turnos
    turno_j1 = 1
    turno_j2 = 1

    salir = False

    #Empieza el J1 con su turno primero

    ServerSocket.sendto(("Turn "+str(turno_j1)).encode("utf-8"),addr_J1)

    while True:
        buffer, addr = ServerSocket.recvfrom(buffersize)

        #Estos pasos se repetiran cada turno del juego.
        move = buffer.decode("utf-8")
        #Fila es igual al numero -1 y la columna es ord(Letra)-65
        f = int(move[1:]) - 1
        c = ord(move[0]) - 65

        #Comprobamos quien de los dos está jugando y los pasos a seguir son similares (explicamos solo los del J1)
        if(addr == addr_J1):
            while True:     #Este bucle se da mientras el J1 vaya acertando barcos rivales
                turno_j1+=1
                if(comprobar_barco(tablero_J2,f,c)):        #Si el movimiento acierta ponemos dicha posicion del tablero rival a 0
                    tablero_J2[f,c]=0
                    
                    if(hay_navios(tablero_J2)):             #Se comprueba que queden navios restantes
                        ServerSocket.sendto(b"Hit",addr_J1)
                        ServerSocket.sendto(("Turn "+str(turno_j1)).encode("utf-8"),addr_J1)
                    else:                                   #Si no los hay el juego acaba y se les manda sus respectivos mensajes a cada uno.
                        print(N_J1 + " WINS THE GAME!")
                        ServerSocket.sendto(b"You win",addr_J1)
                        ServerSocket.sendto(b"You lost",addr_J2)
                        salir = True
                else:                       #Si el jugador falla el movimiento pierde el turno.
                    addr = addr_J2
                    ServerSocket.sendto(b"Fail",addr_J1)
                    ServerSocket.sendto(("Turn "+str(turno_j2)).encode("utf-8"),addr_J2)

                
                break
        elif (addr == addr_J2):
            while True:
                turno_j2+=1
                if(comprobar_barco(tablero_J1,f,c)):
                    tablero_J1[f,c]=0

                    if(hay_navios(tablero_J1)):
                        ServerSocket.sendto(b"Hit",addr_J2)
                        ServerSocket.sendto(("Turn "+str(turno_j2)).encode("utf-8"),addr_J2)
                    else:
                        print(N_J2 + " WINS THE GAME!")
                        ServerSocket.sendto(b"You win",addr_J2)
                        ServerSocket.sendto(b"You lost",addr_J1)
                        salir = True
                else:
                    addr = addr_J1
                    ServerSocket.sendto(b"Fail",addr_J2)
                    ServerSocket.sendto(("Turn "+str(turno_j1)).encode("utf-8"),addr_J1)

                
                break
        else:                       #Caso de error en el que la dirección del mensaje recibido no corresponda con ningun jugador.
            print("[FAIL] Connection failed.")
            ServerSocket.close()
            exit()
        if(salir):              #Si el juego acaba, salimos del bucle.
            print("[INFO] Game has ended")
            break

    print("[FINISH] Connection finished.")
    ServerSocket.close()    #Cerramos la conexión


        





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()

    main(args.host, args.port)
