import asyncio
import logging
from kademlia.network import Server


class KademliaNetwork(Server):

    def __init__(self,*args, **kwargs) -> None:
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log = logging.getLogger('kademlia')
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
        
        super(KademliaNetwork,self).__init__()

    def start(self,is_bootstrap=False,bootstrap_addr = "",bootstrap_port = 8468 ):
        input
        if is_bootstrap:
            loop = asyncio.get_event_loop()
            loop.set_debug(True)

            loop.run_until_complete(self.listen(8468))


            try:
                loop.run_forever()
            except KeyboardInterrupt:
                pass
            finally:
                self.stop()
                loop.close()
        else:
            if bootstrap_addr=="":
                raise Exception("Indiquer l'adresse du noeud bootstrap")
            else:
                async def run():
                    await self.listen(8469)
                    bootstrap_node = (bootstrap_addr, bootstrap_port)
                    await self.bootstrap([bootstrap_node])
                    await self.set("key", "mykey1")
                    self.stop()

                asyncio.run(run()) 

    def getNeighbors(self):
        return self.bootstrappable_neighbors()
