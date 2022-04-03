import argparse
import os
import socket
import sys


def main(host, port, filein, fileout):

    #Abrimos el fichero, obtenemos su tamaño y el contenido lo guardamos en una variable. Por ultimo lo cerramos
    f = open(filein, "r")
    file_size = os.path.getsize(filein)
    mensaje = f.read()
    f.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    #Creamos un socket y intentamos la conexión con el server
        s.connect((host,port))
        s.send((str(file_size)+"\n").encode("utf-8"))       #Le mandamos una primera línea con el tamaño del fichero y de seguido el contenido del fichero
        s.sendall(mensaje.encode("utf-8"))
    

        #Ahora, el cliente recibe la respuesta del servidor
        buff_size = 4096
        
        data_bytes = s.recv(buff_size).decode("utf-8")  #Recibimos un primer mensaje en el que la primera linea es el tamaño del posterior

        aux = data_bytes.split(sep='\n', maxsplit=1) #Lo separamos y los almacenamos en una variable

        size = int(aux[0])
        data = aux[1].encode("utf-8")   #Inicializamos la variable data que contendrá el mensaje total del servidor (en bytes, IMPORTANTE)
            
        while sys.getsizeof(data) <= size:  #Mientras data no supere el tamaño total de la respuesta seguimos leyendo y almacenando
            data += s.recv(buff_size)
                
        #Una vez se lee todo, lo decodificamos
        output = data.decode("utf-8")
            

        print("[RECIEVED] Respond recieved.")

        #Abrimos el otro fichero, escribimos en el y lo cerramos
        f = open(fileout, "w")
        f.write(output)
        f.close()

        print("[FILE] File updated.")

        s.close()       #Cerramos el socket y el programa finaliza

        print("[Finish] Connection finished.")

    

    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="remote port")
    parser.add_argument('--host', default='localhost', help="remote hostname")
    parser.add_argument('--filein', default='filein.txt', help="file to be read")
    parser.add_argument('--fileout', default='fileout.txt', help="file to be written")
    args = parser.parse_args()

    main(args.host, args.port, args.filein, args.fileout)
