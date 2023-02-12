from kademlia.network import Server
import socket
import asyncio
from splitting import Splitting
import os


class Network():

    def __init__(self,address,port,is_bootstrap=False):
        
        self.address = address
        self.port = port
        self.is_bootstrap = is_bootstrap
        self.send_port = port+10000
        self.my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.kademlia_server = Server()
        self.neighbors = []
        self.my_socket.bind((self.address,self.send_port))
        self.my_socket.listen()
        self.BUFFER_SIZE = 16384

    async def socket_connect(self,socket):
        client, address = socket.accept()
        print(f"log===>Client {address} connected")
        filename = "fileTest"
        with open(filename,'wb') as f:
            while(True):
                data = client.recv(self.BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
            os.rename('fileTest',Splitting.fileHash)
    async def run(self):
        try:
            self.kademlia_server = Server()
            await self.kademlia_server.listen(self.port)
            bootstrap_node = ('127.0.0.1', 8468)
            await self.kademlia_server.bootstrap([bootstrap_node])
            print("******************finding******************")
            self.neighbors = self.kademlia_server.bootstrappable_neighbors() 
            print(self.neighbors)

        except KeyboardInterrupt:
            self.kademlia_server.stop()
   
    
    async def start_net(self):
       
        if self.is_bootstrap:
            loop = asyncio.get_event_loop()
            loop.set_debug(True)

            self.kademlia_server
            loop.run_until_complete(self.kademlia_server.listen(self.port))
            await self.socket_connect(self.my_socket)

            try:
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
        
    async def sendFile(self,filename):
        send_socket = socket.socket()

        send_socket.connect((self.address,self.port))
        print(f"Sending file: {filename}")
        with open(filename,'rb') as f:
            while True:
                data = f.read(self.BUFFER_SIZE)
                if not data:
                    break;
                send_socket.send(data)


