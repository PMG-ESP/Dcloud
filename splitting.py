import pickle
import os
import hashlib
import pathlib
from cryptFile import CryptFile




class Splitting():

    def __init__(self,nb_splits,name="",is_folder=False):
        self.is_folder = is_folder
        self.filename = name #nom du fichier pour le split. omettre pour le reassemble 
        self.nb_splits = nb_splits #nombre de filepart à distribuer sur le réseau
        self.file_part_folder = pathlib.Path("fileParts/")
        
        self.BUFFER_SIZE = 4096 #taille du buffer


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


    def split(self):


        #dictionnaire à ecrire dans le fichier manifest
        #fichier manifest contenant les informations pour la reconstitution du fichier original
        self.file_info = {
            "filepath" : self.filename,
            "filename" : self.filename.split("\\")[-1],
            "filehash" : self.fileHash(self.filename),
            "filesize" : os.path.getsize(self.filename),
            "part_list" : []
        }


        self.filesize = self.file_info["filesize"]
        print(f"log===>taille du fichier: {self.filesize}")
        
        #Ouvrir le fichier demande
        try:
            file = open(self.filename,"rb")
        except FileNotFoundError:
            print("Erreur: Fichier introuvable ")
        except EnvironmentError as e:
            print(f"Erreur innatendue: {e}")
        else:
            part_size = (self.filesize/self.nb_splits)
            print(f"log===>partsize: {part_size}")
            nb_reads = int(part_size/self.BUFFER_SIZE)+1
            print(f"log===>nb_reads: {nb_reads}")

            for i in range(self.nb_splits):

                file_part_name = f"filepart{i}"
                os.path.join("fileParts",file_part_name)
                print(f"log===>processing part no{i}")
                with open(self.file_part_folder / file_part_name,"wb") as file_part:

                    for i in range(nb_reads):
                        temp_data = file.read(self.BUFFER_SIZE)
                        if not temp_data:
                            break
                        file_part.write(temp_data)
                #Crypter chaque partie du fichier         
                cryptage = CryptFile(self.file_part_folder / file_part_name,"key")

                #ajouter le hash dans le manifest du fichier
                self.file_info["part_list"].append(cryptage.encrypt())
        finally:
            file.close()

        #creation du fichier manifest            
        manifest_name = self.file_info["filehash"]
        os.path.join("manifest",manifest_name)
        manifest = pathlib.Path("manifest/")
        file = open(manifest / manifest_name,"wb")
        pickle.dump(self.file_info,file)
        file.close()

    @staticmethod
    def dirTree(root, path):
        #recreer l'arborescence a partir du chemin partant de root
        os.path.join(root, path)
        os.makedirs(path)
        
    def reassemble(self,filehash):
        #recuperer le manifest
        try:
            unpickle = open(filehash,'rb') 
            file_info = pickle.load(unpickle)
        except Exception as e:
            print(f"Erreur lors de la recuperation du hash: {e}")
        finally:
            unpickle.close()
        os.path.basename(file_info["filename"])
        
        with open(file_info["filename"],"wb") as file:
            i=0
            for part in file_info["part_list"]:
                part_decrypted = part.split(".crypt")[0]
                part_decrypted = self.file_part_folder / f"{part_decrypted}.decrypt"
                
                part = self.file_part_folder / part
                CryptFile(part ,"key").decrypt()
                with open(part_decrypted,"rb") as file_part:
                    print(f"log===>processing part no{i}")
                    while(True):
                        temp_data = file_part.read(self.BUFFER_SIZE)
                        if not temp_data:
                            break
                        file.write(temp_data)
                    i+=1
                os.remove(part_decrypted)

            
#####TEST
# filenames = [
#     r"testfiles\Bleach Kai - Bleach Kai - 02 VOSTFR - 02 - Voiranime.ts",
#     r"testfiles\78781-one-piece-ace-wallpaper-top-free-one-piece-ace-background.jpg",
#     r"testfiles\Hermetic Wiper- Ukraine Cyberattack Analysis.mp4"
# ]

# for filename in filenames:
#     print(filename)
#     test = Splitting(10,filename)
#     test.split()



#print(test.file_info)

# filehashs = [r"manifest\160126e1067f307cfb2d52713f5ef4879ccb143449bb5cc8804c1589d204cea0",r"manifest\929116c6b54500b6a90a71892c6ebd539aa5ade4d7538868a869ec75969457bf",r"manifest\a80c11e027542918da05340836b38fafcfa0626b9dbbbd3e565ade7ae90d0ae2"]
# test = Splitting(10,filename="")

# for hash in filehashs:
#     test.reassemble(hash)