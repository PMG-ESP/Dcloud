import os
from cryptography.fernet import Fernet
import hashlib
import pathlib

class CryptFile():

    def __init__(self,filename,keyfile) -> None:
        self.filename = filename
        self.file_folder = pathlib.Path('fileParts')
        
        self.h = hashlib.sha256()

        with open(keyfile,"rb") as k:
            key = k.read()
        self.fernet = Fernet(key)

    def encrypt(self):
        # crypter le fichier et le renommer en son hash
        # renvoie le hash du fichier 
        print("log===>Cryptage en cours...")
        with open(self.filename, 'rb') as file:
            print(self.filename)
            crypted_file = os.path.basename(self.filename)
            crypted_file = f"{crypted_file}.crypt"
            os.path.join(self.file_folder,crypted_file)
            with open(self.file_folder / crypted_file,'wb') as cfile:
                temp_data = file.read()
                self.h.update(temp_data)
                cfile.write(self.fernet.encrypt(temp_data))
        os.remove(self.filename)
        try:
            os.rename(self.file_folder / crypted_file, self.file_folder / f"{self.h.hexdigest()}.crypt")
        except FileExistsError:
            pass
        return f"{self.h.hexdigest()}.crypt"

    def decrypt(self):

        print("log===>decryptage en cours...")
        
        #decrypter le fichier 
        with open(self.filename, 'rb') as cfile:
            decrypted_file = os.path.basename(self.filename)
            decrypted_file = decrypted_file.split(".crypt")[0]
            decrypted_file = f"{decrypted_file}.decrypt"
            os.path.join(self.file_folder,decrypted_file)
            with open(self.file_folder / decrypted_file, 'wb') as file:
                temp_data = cfile.read()
                file.write(self.fernet.decrypt(temp_data))
        os.remove(self.filename)
    
    
        


#############TEST#######################
# filename = r"testfile.txt"

# test = CryptFile(r"testfile.txt","key")
# test.encrypt()

# test = CryptFile("aa31ee83cdaa3e93750a17d4b5bea9e682768ccc474dbb1bfe5eea11a4502f82.crypt","key")
# test.decrypt()
