__author__ = 'kalo'
from SerialManager import SerialManager
from Events import Events
from  WebComunication import WebComunication
import threading
import Queue
from urllib import *
import websocket


class Manager():
    def __init__(self, host, port):
        self.stop_event = threading.Event()
        self.to_serial = Queue.Queue()
        self.from_serial = Queue.Queue()
        self.to_web = Queue.Queue()
        self.from_web = Queue.Queue()
        # self.serial_manager = SerialManager("/dev/ttyACM0", 9600, "/dev/ttyUSB0", 9600,
        #                                     self.stop_event,
        #                                     self.to_serial, self.from_serial)
        self.web_com = WebComunication("10.0.202.13", 8080, self.to_web, self.from_web, self.stop_event)


man = Manager("10.0.202.13", 8080)

