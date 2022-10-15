from http import client
import socket
class Upload():
    def __init__(self,filename,host,port) -> None:
        self.filename = filename
        self.host = host
        self.port = port

    def start(self):

        tcp_socket = socket.socket()
        tcp_socket.bind((self.host,self.port))
        tcp_socket.listen()

        client = tcp_socket.accept()
        print("client connecté")

        
