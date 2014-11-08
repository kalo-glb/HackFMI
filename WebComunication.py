__author__ = 'kalo'
import threading
from urllib import *
import websocket


class WebComunication(threading.Thread):
    def __init__(self, host, port, in_queue, out_queue, stop_event):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.init_server()

    def init_server(self):
        (sid, hbtimeout, ctimeout) = self.handshake(self.host, self.port)
        self.server = websocket.create_connection("ws://%s:%d/socket.io/1/websocket/%s" % (self.host, self.port, sid))
        print(self.server.recv())
        self.server.send("2::")
        self.server.send('5:1::{"name":"getPattern", "args":"system_ready"}')
        while True:
            asd = self.server.recv()
            #if asd != "":
            print(asd)
                #break

    def handshake(self, host, port):
        u = urlopen("http://%s:%d/socket.io/1/" % (host, port))
        if u.getcode() == 200:
            response = u.readline()
            (sid, hbtimeout, ctimeout, supported) = response.split(":")
            supportedlist = supported.split(",")
            if "websocket" in supportedlist:
                return (sid, hbtimeout, ctimeout)
            else:
                raise TransportException()
        else:
            raise InvalidResponseException()