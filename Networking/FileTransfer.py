import socket
import threading
import os
import hashlib


class FileTransfer():
    def __init__(self,host) -> None:
        self.host = host
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.BUFFER_SIZE = 16384
        
    
    @staticmethod
    def fileHash(filename):
        # calcule et renvoie le hash sha256 d'un fichier 
        h = hashlib.sha256()
        try: 
            f = open(filename,'rb')
        except FileNotFoundError: 
            return "Fichier introuvable"
        except :
            return "erreur inattendu l'ors de l'ouverture du fichier"
        else:
            h.update(f.read())
            return h.hexdigest()
        finally:
            f.close()
    
    def _receive(self):
        try:
            self.sock.bind(self.host)
            self.sock.listen()
        except Exception:
            self.sock.close()
            print("Erreur innatendue lors de la creation du socket")
        client, address = self.sock.accept()
        print(f"log===>Client {address} connected")
        filename = "fileTest"
        with open(filename,'wb') as f:
            while(True):
                data = client.recv(self.BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
            os.rename('fileTest',self.fileHash("fileTest"))
    def receive(self):
        thread_receive = threading.Thread(self._receive)
        thread_receive.start()

    def _send_file(self,socket,filename):
        with open(filename,'rb') as f:
            while True:
                data = f.read(self.BUFFER_SIZE)
                if not data:
                    break;
                try:
                    socket.send(data)
                except Exception:
                    socket.close()
                    f.close()
                    print("Erreur lors de l'envoie des données")

    def _send(self,neighbors_list,file_list):


        send_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        if len(file_list)!=0 or len(neighbors_list)!=0:
            raise Exception("neighbors_list ou file_list vide !")
        
        for file in file_list:
            index = file_list.index(file)%len(neighbors_list)
            send_socket.connect(neighbors_list[index])

    def send(self):
        thred_send = threading.Thread(self._send)
        thred_send.start()

    

