import argparse
from os import sep
import socket
import sys



def main(host, port):
    print("[STARTING] Server is starting.")
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:     #Creamos un primer socket que será el de control
        s.bind((host,port))
        s.listen()  #Comienza la espera de una conexión
        print("[LISTENING] Server is listening.")

        conn, addr = s.accept()     #La aceptamos y tenemos el socket conn.
        print(f"[NEW CONECTION] {addr} connected.")

        with conn:

            buff_size = 4096

            data_bytes = conn.recv(buff_size).decode("utf-8")   #Recibimos un mensaje inicial, en el que la primera línea contiene el tamaño de lo que tiene que recibirse
            aux = data_bytes.split(sep='\n', maxsplit=1)    #Lo separamos y guardamos en una variable

            size = int(aux[0])
            data = aux[1].encode("utf-8")        #Inicializamos la variable data que contendrá el mensaje total del servidor (en bytes, IMPORTANTE)
            
            while sys.getsizeof(data) <= size:      #Mientras data no supere el tamaño total de la respuesta seguimos leyendo y almacenando
                data += conn.recv(buff_size)    
                
            #Una vez se lee todo, lo decodificamos
            output = data.decode("utf-8")


            print("[RECIEVE] File recieved.")

            #Empieza la parte del programa encargada de encontrar las palabras con a
            n_A = 0
            frecuencia = ""

            for palabra in output.split():      #Buscamos palabra a palabra y la vamos incluyendo en el string output separadas por \n
                            
                if 'a' in palabra or 'A' in palabra:
                    check_word = palabra.split(sep = ',')
                    n_A  += 1                   #Tambien incrementamos el numero de palabras
                    frecuencia += "\n" + str(check_word[0])

            
            #Elaboramos el mensaje de respuesta que se va a enviar
            #Una primera línea con el numero de palabras
            answer = str(n_A) + " Words with [a|A]: \n" 

            if n_A > 0: #Si el numero de palabras encontradas es > 0 le añadimos la lista de las palabras
                answer += frecuencia 
                    
            print("[OPERATION] File treated.")

            print("[SENDING] Sending answer")

            answer_size = sys.getsizeof(answer)    
            conn.send((str(answer_size)+"\n").encode("utf-8")) #En el mesnaje añadimos una linea inicial con el tamaño en bytes que se envian
            conn.sendall(answer.encode("utf-8"))
            
            print ("[TRANSFER] File transfered.")

            print ("[FINISH] Connection finished.")
            
            conn.close() #Cerramos el socket conn

        s.close() #Cerramos la conexion y el programa finaliza
                
        

    





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()

    main(args.host, args.port)
