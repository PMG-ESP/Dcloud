import logging
import asyncio
import sys
from kademlia.crawling import NodeSpiderCrawl

from kademlia.network import Server

# if len(sys.argv) != 5:
#     print("Usage: python set.py <bootstrap node> <bootstrap port> <key> <value>")
#     sys.exit(1)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)
with open("test.txt","rb") as f:
    data = f.read()

async def run():
    try:
        server = Server()
        await server.listen(8470)
        bootstrap_node = ('127.0.0.1', 8468)
        await server.bootstrap([bootstrap_node])
        nearest = server.protocol.router.find_neighbors(server.node, server.alpha)
        #spider = NodeSpiderCrawl(server.protocol,server.node,nearest,server.ksize,server.alpha)
        print("******************finding******************")
        print(server.bootstrappable_neighbors())
        #await spider.find()
        #await server.get("keynodeubuntu")
    except KeyboardInterrupt:
        server.stop()


asyncio.run(run())