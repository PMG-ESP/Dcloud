import os
from cryptFile import CryptFile
class Splitting():

    def __init__(self,nb_splits,filename):
        self.filename = filename
        self.nb_splits = nb_splits
        self.file_info = {
            "filename" : self.filename,
            "filesize" : os.path.getsize(self.filename),
            "part_list" : []
        }
        self.BUFFER_SIZE = 4096

    def split(self):
        self.filesize = os.path.getsize(self.filename)
        print(f"log===>taille du fichier: {self.filesize}")

        with open(self.filename,"rb") as file:

            part_size = (self.filesize/self.nb_splits)
            print(f"log===>partsize: {part_size}")
            nb_reads = int(part_size/self.BUFFER_SIZE)+1
            print(f"log===>nb_reads: {nb_reads}")

            for i in range(self.nb_splits):

                file_part_name = os.path.basename(f"filepart{i}")
                print(f"log===>processing part no{i}")
                with open(file_part_name,"wb") as file_part:

                    for i in range(nb_reads):
                        temp_data = file.read(self.BUFFER_SIZE)
                        if not temp_data:
                            break
                        file_part.write(temp_data)
                cryptage = CryptFile(file_part_name,"key")
                self.file_info["part_list"].append(cryptage.encrypt())
        #os.remove(self.filename)
        
    def reassemble(self):
        os.path.basename(self.filename)
        with open(self.filename,"wb") as file:

            for i in range(self.nb_splits):

                file_part_name = f"filepart{i}"
                print(f"log===>processing part no{i}")
                with open(file_part_name,"rb") as file_part:

                    while(True):
                        temp_data = file_part.read(self.BUFFER_SIZE)
                        if not temp_data:
                            break
                        file.write(temp_data)
                
            for i in range(self.nb_splits):
                print("deleting the file")
                os.remove(f"filepart{i}")            

            
#####TEST
filename = r"testfiles\Bleach Kai - Bleach Kai - 02 VOSTFR - 02 - Voiranime.ts"
test = Splitting(10,filename)
test.split()
print(test.file_info)
#test.reassemble()