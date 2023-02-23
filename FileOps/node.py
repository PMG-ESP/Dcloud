from capacityException import CapacityException
import uuid
import os
import socket
import json


class Node:

    def __init__(self,zone,capacity,**args):
        self.zone = zone 
        self.capacity=capacity #espace de stockage disponible
        self.id = zone + str(uuid.uuid1()) #identifiant unique
        print(f"ID du noeud: {self.id}")
        new_folder = r'.\CloudFiles' #Dossier pour stocker les shards et manifests
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        
    #verifier si la capacité est suffisante
    def checkCapacity(self,required_capacity):

        if(self.capacity<required_capacity):
            self.capacity -= required_capacity
        else:
            raise CapacityException("capacité insuffisante")

    
    def online(self,addr,port):
        
        mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creeation socket TCP
        mysocket.bind((addr,port))
        print("Waiting for connection") # attente de connexion
        try:
            mysocket.listen()
        

        try:
            conn, addr = mysocket.accept()
            print(f"client :  {addr} connected")
        except Exception as e:
            mysocket.close()
            print(f"Erreur lors de la connexion: {e}")
        
        node_info =  {
            "id": self.id,
            "capacity": self.capacity
        }

        infos = json.dumps(node_info).encode("utf-8")
        try:
            conn.sendall(infos)
        except Exception as e:
            try:
                conn.close()
            except:
                pass
            mysocket.close()
            print("Erreur lors de l'envoie des infos")

        print("Node infos sent succesfully")

    def getNodes(self,addr,port):

        mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            mysock.connect(addr,port)
        except Exception as e:
            mysock.close()
            print(f"Erreur lors de la connexion: {e}")
        print(f"connected to the node {addr}:{port}")
        


        
        



