import argparse
import socket
import math
import re

def f(x):
    return math.sqrt(1 - math.pow(x,2))

def main(host, port):

    serv_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    serv_udp.bind((host,port))


    while (True):
        mensaje,addr = serv_udp.recvfrom(1024)

        msj = (mensaje.decode("utf-8"))

        if (msj != "exit"):
    
            x = msj[1:msj.find(",")]
            y = msj[msj.find(",")+1:-2]

            x = float(x)
            y = float(y)

            if y < 0 or y > 1:
                serv_udp.sendto("error".encode("utf-8"),addr)
            elif y < f(x):
                serv_udp.sendto("below".encode("utf-8"),addr)
            else:
                serv_udp.sendto("above".encode("utf-8"),addr)
        else:
            break
    
    serv_udp.close()
    
    




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()

    main(args.host, args.port)
