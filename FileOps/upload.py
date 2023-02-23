from http import client
import socket
class Upload():
    def __init__(self,filename,host) -> None:
        self.filename = filename
        self.host = host
        self.port = 8687
        self.buffer = 16384

    def availableNodes(self):
        