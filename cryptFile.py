import os
from cryptography.fernet import Fernet
import hashlib

class CryptFile():

    def __init__(self,filename,keyfile) -> None:
        self.filename = filename
        
        self.h = hashlib.sha256()

        with open(keyfile,"rb") as k:
            key = k.read()
        self.fernet = Fernet(key)

    def encrypt(self):
        
        print("log===>Cryptage en cours...")
        with open(self.filename, 'rb') as file:
            crypted_file = f"{self.filename}.crypt"
            os.path.basename(crypted_file)
            with open(crypted_file,'wb') as cfile:
                temp_data = file.read()
                self.h.update(temp_data)
                cfile.write(self.fernet.encrypt(temp_data))
        os.remove(self.filename)
        os.rename(crypted_file,self.h.hexdigest())
        return self.h.hexdigest()
    
    def decrypt(self):

        crypted_file = f"{self.filename}.crypt"
        os.path.basename(self.filename)
        print("log===>decryptage en cours...")
        with open(crypted_file, 'rb') as cfile:

            with open(self.filename, 'wb') as file:
                
                temp_data = cfile.read()
                file.write(self.fernet.decrypt(temp_data))
        os.remove(crypted_file)
    
    
        


#############TEST#######################
# filename = r"testfile.txt"

# test = CryptFile(r"testfile.txt","key")
# test.encrypt()
# # test.decrypt()
