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
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.stop_event = stop_event
        self.wait_for_response = 0

    def init_server(self):
        (sid, hbtimeout, ctimeout) = self.handshake(self.host, self.port)
        self.server = websocket.create_connection("ws://%s:%d/socket.io/1/websocket/%s" % (self.host, self.port, sid))
        print(self.server.recv())
        self.server.send("2::")

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
                data = self.in_queue.get(block=False)
                self.init_server()
                print(str(data[1]))
                self.server.send('5:1::{"name":"' + data[0] + '", "args":"' + str(data[1]) + '"}' )
                if data[0] == "getPattern":
                    self.wait_for_response = 2
                elif data[0] == "end" or data[0] == "playerError":
                    self.wait_for_response = 1
                else:
                    self.wait_for_response = 2
            if 0 != self.wait_for_response:
                self.wait_for_response -= 1
                recieved_data = self.server.recv()
                print("log: %s" % recieved_data)
                if recieved_data[0] == '3':
                    pattern = recieved_data.split(':')[-1]
                    self.out_queue.put(pattern)

                if self.wait_for_response == 0:
                    self.server.close()

            time.sleep(0.001)