import argparse
import socket
import numpy as np

#Funcion que comprueba si acierta el tiro
def comprobar_barco(tablero_rival,fila,columna):
    if(tablero_rival[fila,columna] == 1):
        return True
    else:
        return False

#Funcion que comprueba si hay navios restantes
def hay_navios(tablero_rival):
    awnser = False
    for f in range(10):
        for c in range(10):
            if tablero_rival[f,c]==1:
                awnser = True
                return awnser

    return awnser

def main(host, port):
    buffersize = 1024
    ServerSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    ServerSocket.bind((host,port))

    print("[Starting] Server UP and waiting players.")

    BytesJ1,addr_J1 = ServerSocket.recvfrom(buffersize)
    N_J1 = BytesJ1.decode("utf-8")
    print(N_J1+" has joined the game (Address: "+ str(addr_J1) + " )") 

    BytesJ1,addr_J1 = ServerSocket.recvfrom(buffersize)
    tablero_J1 = BytesJ1.decode("utf-8")
    print(N_J1+"'s Board has been recieved.")

    BytesJ2,addr_J2 = ServerSocket.recvfrom(buffersize)
    N_J2 = BytesJ2.decode("utf-8")
    print(N_J2+" has joined the game (Address: "+ str(addr_J2) + " )")

    BytesJ2, addr_J2 = ServerSocket.recvfrom(buffersize)
    tablero_J2 = BytesJ2.decode("utf-8")
    print(N_J2+"'s Board has been recieved.")

    #----DATOS RECIBIDOS----#

    tablero_J1 = np.matrix(tablero_J1,int)
    tablero_J2 = np.matrix(tablero_J2, int)

    turno_j1 = 1
    turno_j2 = 1

    salir = False

    #Empieza el J1 y el juego

    ServerSocket.sendto(("Turn "+str(turno_j1)).encode("utf-8"),addr_J1)

    while True:
        buffer, addr = ServerSocket.recvfrom(buffersize)

        move = buffer.decode("utf-8")
        #Fila es igual al numero -1 y la columna es ord(Letra)-65
        f = int(move[1]) - 1
        c = ord(move[0]) - 65

        if(addr == addr_J1):
            while True:
                turno_j1+=1
                if(comprobar_barco(tablero_J2,f,c)):
                    tablero_J2[f,c]=0
                    
                    if(hay_navios(tablero_J2)):
                        ServerSocket.sendto(b"Hit",addr_J1)
                        ServerSocket.sendto(("Turn "+str(turno_j1)).encode("utf-8"),addr_J1)
                    else:
                        ServerSocket.sendto(b"You win",addr_J1)
                        ServerSocket.sendto(b"You lost",addr_J2)
                        salir = True
                else:
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
                        ServerSocket.sendto(b"You win",addr_J2)
                        ServerSocket.sendto(b"You lost",addr_J1)
                        salir = True
                else:
                    addr = addr_J1
                    ServerSocket.sendto(b"Fail",addr_J2)
                    ServerSocket.sendto(("Turn "+str(turno_j1)).encode("utf-8"),addr_J1)

                
                break
        else:
            print("[FAIL] Connection failed.")
            ServerSocket.close()
            exit()
        if(salir):
            print("[INFO] Game has ended")
            break

    print("[FINISH] Connection finished.")
    ServerSocket.close()


        





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()

    main(args.host, args.port)
