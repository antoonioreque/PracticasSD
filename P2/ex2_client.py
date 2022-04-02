import argparse
import os
import socket
import sys


def main(host, port, filein, fileout):

    f = open(filein, "r")
    file_size = os.path.getsize(filein)
    mensaje = f.read()
    f.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host,port))
        s.send((str(file_size)+"\n").encode("utf-8"))
        s.sendall(mensaje.encode("utf-8"))
    

        buff_size = 4096
        
        data_bytes = s.recv(buff_size).decode("utf-8")

        aux = data_bytes.split(sep='\n', maxsplit=1)

        size = int(aux[0])
        data = aux[1].encode("utf-8")
            
        while sys.getsizeof(data) <= size:
            data += s.recv(buff_size)
                
            
        output = data.decode("utf-8")
            

        print("[RECIEVED] Respond recieved.")

        f = open(fileout, "w")
        f.write(output)
        f.close()

        print("[FILE] File updated.")

        s.close()

        print("[Finish] Connection finished.")

    

    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="remote port")
    parser.add_argument('--host', default='localhost', help="remote hostname")
    parser.add_argument('--filein', default='filein.txt', help="file to be read")
    parser.add_argument('--fileout', default='fileout.txt', help="file to be written")
    args = parser.parse_args()

    main(args.host, args.port, args.filein, args.fileout)
