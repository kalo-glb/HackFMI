__author__ = 'kalo'
from SerialManager import SerialManager
from Events import Events, EventTypes
from WebComunication import WebComunication
import threading
import Queue
import time


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
        self.serial_manager.start()
        self.web_com.start()
        while True:
            if not self.from_serial.empty():
                data = ("error", "error")
                event = self.from_serial.get(block=False)
                if event["event_type"] == EventTypes.rfid_event:
                    #print("debug: getPattern")
                    self.time_start = time.time()
                    data = ("getPattern", event["e"])
                if event["event_type"] == EventTypes.mcu_event:
                    if event["e"] == Events.player_won:
                        #print("debug: end")
                        data = ("end", time.time() - self.time_start)
                    elif event["e"] == Events.player_error:
                        data = ("playerError", time.time() - self.time_start)

                if data[1] != "error":
                    self.to_web.put(data)

            if not self.from_web.empty():
                self.to_serial.put(self.from_web.get())

            time.sleep(0.01)


man = Manager("192.168.0.101", 8080)
man.run()

