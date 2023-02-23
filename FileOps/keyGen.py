import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class KeyGen():

    def __init__(self,filename,password) -> None:
        self.filename = filename
        self.password = password
        password = bytes(self.password, 'utf8')
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.fernet = Fernet(key)

        with open(filename,"wb") as k:
            k.write(key)

##TEST##

keytest = KeyGen("key","passer123")