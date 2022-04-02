import argparse
from os import sep
import socket
import sys



def main(host, port):
    print("[STARTING] Server is starting.")
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((host,port))
        s.listen()
        print("[LISTENING] Server is listening.")

        conn, addr = s.accept()
        print(f"[NEW CONECTION] {addr} connected.")

        with conn:

            buff_size = 4096

            data_bytes = conn.recv(buff_size).decode("utf-8")
            aux = data_bytes.split(sep='\n', maxsplit=1)

            size = int(aux[0])
            data = aux[1].encode("utf-8")
            
            while sys.getsizeof(data) <= size:
                data += conn.recv(buff_size)
                
            
            output = data.decode("utf-8")


            print("[RECIEVE] File recieved.")

            n_A = 0
            frecuencia = ""

            for palabra in output.split():
                            
                if 'a' in palabra or 'A' in palabra:
                    check_word = palabra.split(sep = ',')
                    n_A  += 1
                    frecuencia += "\n" + str(check_word[0])

            

            answer = str(n_A) + " Words with [a|A]: \n" 

            if n_A > 0:
                answer += frecuencia 
                    
            print("[OPERATION] File treated.")

            print("[SENDING] Sending answer")

            answer_size = sys.getsizeof(answer)    
            conn.send((str(answer_size)+"\n").encode("utf-8")) #En el mesnaje añadimos una linea inicial con el tamaño en bytes que se envian
            conn.sendall(answer.encode("utf-8"))
            
            print ("[TRANSFER] File transfered.")

            print ("[FINISH] Connection finished.")
            
            conn.close()

        s.close()
                
        

    





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()

    main(args.host, args.port)
