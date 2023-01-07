import os
from splitting import Splitting
import time

start_time = time.time()


path  = r"C:\Users\PC\Documents\PMG's SD Card"
filelist = []

for root, dirs, files in os.walk(path):
	for file in files:
        #append the file name to the list
		filelist.append(os.path.join(root,file))

#print all the file names
for name in filelist:
    print(name)
    test = Splitting(10,name)
    test.split()

print("--- %s seconds ---" % (time.time() - start_time))