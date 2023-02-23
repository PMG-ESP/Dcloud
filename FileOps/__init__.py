from splitting import Splitting
import time
import pickle
import asyncio

start_time = time.time() #timer


#net = Network("127.0.0.1",8468,True)
#asyncio.run(net.start_net())


def upload():
    filename = r"testfiles\Hermetic Wiper- Ukraine Cyberattack Analysis.mp4"
    #filehashs = r"manifest\160126e1067f307cfb2d52713f5ef4879ccb143449bb5cc8804c1589d204cea0"
    test = Splitting(10,filename)
    info = test.split()
    print(info)
    #net = Network("127.0.0.1",8667,True)

def download():
    filehashs = [r"manifest\929116c6b54500b6a90a71892c6ebd539aa5ade4d7538868a869ec75969457bf"]
    test = Splitting(10)

    for hash in filehashs:
        test.reassemble(hash)

download()
print("Temps d'execution--- %s seconds ---" % (time.time() - start_time))