import hashlib
from kademlia.network import Server
import socket
import threading
import os
import asyncio


class Network():

    def __init__(self,address,port,is_bootstrap=False):
        
        if not is_bootstrap:
            try:
                self.bootstrap_addr = input("Adresse ip du bootstrap node")
                self.bootstrap_port = input("port du bootstrap node")
            except KeyboardInterrupt:
                print("Veuillez saisir l'adresse ip et le port do bootstrap")
        self.address = address
        self.port = port
        self.is_bootstrap = is_bootstrap
        self.send_port = port+10000
        self.my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.kademlia_server = Server()
        self.neighbors = []
        print(f"Binding on {self.address}:{self.send_port}")
        self.my_socket.bind((self.address,self.send_port))
        self.my_socket.listen()
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
    
    def socketConnect(self,socket):
        client, address = socket.accept()
        print(f"log===>Client {address} connected")
        filename = "fileTest"
        with open(filename,'wb') as f:
            while(True):
                data = client.recv(self.BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
            os.rename('fileTest',self.fileHash("fileTest"))

    async def run(self):
        try:
            self.kademlia_server = Server()
            await self.kademlia_server.listen(self.port)
            bootstrap_node = (self.bootstrap_addr, self.bootstrap_port)
            await self.kademlia_server.bootstrap([bootstrap_node])
            print("******************finding******************")
            self.neighbors = self.kademlia_server.bootstrappable_neighbors() 
            print(self.neighbors)

        except KeyboardInterrupt:
            self.kademlia_server.stop()
   
    
    async def _startNet(self):
        print(self.is_bootstrap)
        if self.is_bootstrap:
            print("Starting bootstrap")
            loop = asyncio.get_event_loop()
            loop.set_debug(True)

            self.kademlia_server
            loop.run_until_complete(self.kademlia_server.listen(self.port))
            await self.socketConnect(self.my_socket)

            try:
                print("Starting bootstrap node...")
                loop.run_forever()
            except KeyboardInterrupt:
                pass
            finally:
                self.my_socket.close()
                self.kademlia_server.stop()
                loop.close()
        else:
            await self.socket_connet(self.my_socket)
            asyncio.run(self.run())
    
    def startNet(self):
        asyncio.ensure_future(self._startNet())

    async def _sendFile(self,filename):
        send_socket = socket.socket()

        send_socket.connect((self.address,self.port))
        print(f"Sending file: {filename}")
        with open(filename,'rb') as f:
            while True:
                data = f.read(self.BUFFER_SIZE)
                if not data:
                    break;
                send_socket.send(data)
    def sendFile(self,filename):
        asyncio.ensure_future(self._sendFile(filename))



