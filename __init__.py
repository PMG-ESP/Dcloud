from Networking.net_node import Network
from splitting import Splitting
import time
import pickle


start_time = time.time() #timer

# net = Network("127.0.0.1",8468,True)
# net.start_net


def upload():
    filename = r"C:\Users\pmgue\Documents\Codes\python\DCloud\testfiles\Bleach Kai - Bleach Kai - 02 VOSTFR - 02 - Voiranime.ts"
    #filehashs = r"manifest\160126e1067f307cfb2d52713f5ef4879ccb143449bb5cc8804c1589d204cea0"
    test = Splitting(10,filename)
    info = test.split()
    print(info)
    net = Network("127.0.0.1",8667,True)

def download():
    filehashs = [r"manifest\160126e1067f307cfb2d52713f5ef4879ccb143449bb5cc8804c1589d204cea0"]
    test = Splitting(10)

    for hash in filehashs:
        test.reassemble(hash)

#upload()
print("Temps d'execution--- %s seconds ---" % (time.time() - start_time))