import argparse
import random
import math
import socket


def main(host, port, n):

    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    below_counter = 0

    for i in range (0,int(n)):

        x = random.uniform(0,1)
        y = random.uniform(0,1)
        
        
        mensaje = ("(" + str(x) + "," + str(y) + ")")

        s_udp.sendto(mensaje.encode("utf-8"),(host,port))

        respuesta,addr = s_udp.recvfrom(1024)
        
        if respuesta.decode("utf-8") == "below":
            below_counter += 1
         

    pi = 4.0 * float(below_counter)/float(n)
    print("El valor aproximado de pi con " + str(n) + " puntos aleatorios es: " + str(pi))

    s_udp.sendto("exit".encode("utf-8"),addr)
    s_udp.close()   





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="remote port")
    parser.add_argument('--host', default='localhost', help="remote hostname")
    parser.add_argument('--number', default=100000, help="number of random points to be generated")
    args = parser.parse_args()

    main(args.host, args.port, args.number)
