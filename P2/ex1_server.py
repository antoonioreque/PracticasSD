import argparse
import socket
import math
import re

#Función matematica que nos devuelve un float que determinara si el punto que ha llegado está por encima o por debajo de la función.
def f(x):
    return math.sqrt(1 - math.pow(x,2))

def main(host, port):

    #Creamos el socket y lo enlazamos a la IP y puerto correspondiente
    serv_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    serv_udp.bind((host,port))


    while (True):       #Este bucle se mantiene mientras el cliente envie puntos.
        mensaje,addr = serv_udp.recvfrom(1024)

        msj = (mensaje.decode("utf-8"))     #Descodificamos el mensaje que nos dará el punto.

        if (msj != "exit"): #Condición de salida: Que el cliente nos envíe la palabra 'exit'
            
            #Extraemos del mensaje los numeros decimales x e y
            x = msj[1:msj.find(",")]
            y = msj[msj.find(",")+1:-2]

            x = float(x)
            y = float(y)

            if y < 0 or y > 1:  #Si el cliente envia un x o y mayor que 1 o menos que 0 el servidor devuelve 'error'
                serv_udp.sendto("error".encode("utf-8"),addr)
            elif y < f(x):  #Si no, se comprueba que el punto y recibido sea menor que la funcion f(x) y se envia below
                serv_udp.sendto("below".encode("utf-8"),addr)
            else:       #Si no se envia above
                serv_udp.sendto("above".encode("utf-8"),addr)
        else:
            break
    
    serv_udp.close()    #Se cierra el socket y finaliza el programa
    
    




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()

    main(args.host, args.port)
