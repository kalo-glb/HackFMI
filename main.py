__author__ = 'kalo'
from SerialManager import SerialManager
from Events import Events
from  WebComunication import WebComunication
import threading
import Queue
import time
from urllib import *
import websocket


class Manager():
    def __init__(self, host, port):
        self.stop_event = threading.Event()
        self.to_serial = Queue.Queue()
        self.from_serial = Queue.Queue()
        self.to_web = Queue.Queue()
        self.from_web = Queue.Queue()
        self.serial_manager = SerialManager("/dev/ttyACM0", 9600, "/dev/ttyUSB0", 9600,
                                            self.stop_event,
                                            self.to_serial, self.from_serial)
        self.web_com = WebComunication(host, port, self.to_web, self.from_web, self.stop_event)

    def run(self):
        self.web_com.start()
        self.serial_manager.start()
        while True:
            if not self.from_serial.empty():
                event = self.from_serial.get(block=False)
                if event["event_type"] == Events.rfid_event:
                    self.to_web.put(event["e"])

            if not self.from_web.empty():
                self.to_serial.put(self.from_web.get())

            time.sleep(0.001)


man = Manager("10.0.202.13", 8080)
man.run()

