import argparse
import random
import math
import socket


def main(host, port, n):

    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Creamos el socket UDP
    below_counter = 0                                        #Creamos una variable que almacenara el numero de veces que el server nos devuelve below 

    for i in range (0,int(n)): #Bucle de 0 al numero de puntos que se indica en la llamada del cliente

        x = random.uniform(0,1) #Creamos el punto (x,y) aleatorio entre 0-1
        y = random.uniform(0,1)
        
        #Generamos el mensaje en el formato indicado
        mensaje = ("(" + str(x) + "," + str(y) + ")")

        s_udp.sendto(mensaje.encode("utf-8"),(host,port))   #Enviamos el mensaje

        respuesta,addr = s_udp.recvfrom(1024)   #Recibimos la respuesta que puede ser below, above o error
        
        if respuesta.decode("utf-8") == "below":    #Si es below incrementamos el contador
            below_counter += 1
         

    #Una vez finalizado la interacción con el servidor, calculamos el valor aproximado de pi, con la siguiente formula:
    pi = 4.0 * float(below_counter)/float(n)
    print("El valor aproximado de pi con " + str(n) + " puntos aleatorios es: " + str(pi))

    #Le enviamos el mensaje exit al servidor para que cierre la conexión
    s_udp.sendto("exit".encode("utf-8"),addr)
    s_udp.close()   





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="remote port")
    parser.add_argument('--host', default='localhost', help="remote hostname")
    parser.add_argument('--number', default=100000, help="number of random points to be generated")
    args = parser.parse_args()

    main(args.host, args.port, args.number)
