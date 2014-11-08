__author__ = 'kalo'
from SerialManager import SerialManager
from Events import Events
import threading
import Queue
from urllib import *
import websocket
import json


class Manager():
    def __init__(self, host, port):
        self.stop_event = threading.Event()
        self.to_serial = Queue.Queue()
        self.from_serial = Queue.Queue()
        self.serial_manager = SerialManager("/dev/ttyACM0", 9600, "/dev/ttyUSB0", 9600,
                                            self.stop_event,
                                            self.to_serial, self.from_serial)
        (sid, hbtimeout, ctimeout) = self.handshake(host, port)
        self.server = websocket.create_connection("ws://%s:%d/socket.io/1/websocket/%s" % (host, port, sid))
        print(self.server.recv())
        self.server.send("2::")
        self.server.send('5:1::{"name":"event", "args":"system_ready"}')
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

man = Manager("192.168.100.3", 8080)

