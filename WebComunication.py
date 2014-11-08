__author__ = 'kalo'
import threading
from urllib import *
import websocket
import time


class WebComunication(threading.Thread):
    def __init__(self, host, port, in_queue, out_queue, stop_event):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.init_server()
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.stop_event = stop_event
        self.wait_for_response = 0

    def init_server(self):
        (sid, hbtimeout, ctimeout) = self.handshake(self.host, self.port)
        self.server = websocket.create_connection("ws://%s:%d/socket.io/1/websocket/%s" % (self.host, self.port, sid))
        print(self.server.recv())
        self.server.send("2::")
        self.server.send('5:1::{"name":"start", "args":"system_ready"}')
        print(self.server.recv())
        print(self.server.recv())

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

    def run(self):
        while not self.stop_event.is_set():
            if not self.in_queue.empty():
                self.server.send('5:1::{"name":"getPattern", "args":"%s"}' % self.in_queue.get(block=False))
                self.wait_for_response = 2
            if self.wait_for_response:
                self.wait_for_response -= 1
                asd = self.server.recv()
                #print("log: %s" % asd)
                if asd[0] == '3':
                    pattern = asd.split(':')[-1]
                    self.out_queue.put(pattern)

            time.sleep(0.001)