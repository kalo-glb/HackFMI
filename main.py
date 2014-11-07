__author__ = 'kalo'
import serial
import threading
import queue
import socket
import sys
from urllib import *
import websocket
import json


class Events:
    set_pattern = 0
    start_game = 1
    end_game = 2
    first_sensor_hit = 3
    second_sensor_hit = 4
    third_sensor_hit = 5
    fourth_sensor_hit = 6
    mcu_event = 7
    rfid_event = 8


class SerialManager(threading.Thread):
    __msg_start_char__ = '\x02'
    __msg_end_char__ = b'\x03'
    __msg_len = 15

    def __init__(self, mcu_serial_port, mcu_baud_rate, rfid_port, rfid_baud_rate, stop_event, in_queue, out_queue):
        threading.Thread.__init__(self)
        #self.mcu = serial.Serial(mcu_serial_port, mcu_baud_rate)
        #self.rfid = serial.Serial(rfid_port, rfid_baud_rate)
        self.rfid_buffer = list()
        self.stop_event = stop_event
        self.in_queue = in_queue
        self.out_queue = out_queue

    def set_sensor_pattern(self, pattern):
        self.mcu.write(pattern)

    def incoming_data_read(self):
        card_id = ""
        for cnt in range(self.__msg_len):
            char = self.rfid_buffer.pop()
            if char == self.__msg_start_char__:
                self.rfid_buffer.clear()
                break
            if char == '\r' or char == '\n':
                continue

            card_id += str(char)

        card_id = card_id[::-1]  # reverse string

        return card_id

    def write_to_manager(self, event_type, e, data=None):
        if data is None:
            msg = {"event_type": event_type, "e": e}
        else:
            msg = {"event_type": event_type, "e": e}

        self.out_queue.write(msg)

    def process_card_id(self, card_id):
        self.write_to_manager(Events.rfid_event, card_id)

    def process_mcu_event(self, event):
        self.write_to_manager(Events.mcu_event, event)

    def process_control_event(self, event):
        pass

    def run(self):
        while not self.stop_event.is_set():
            if self.mcu.inWaiting():
                e = self.mcu.read()
                self.process_mcu_event(e)
            if self.rfid.inWaiting():
                char_buf = self.rfid.read()
                if char_buf != self.__msg_end_char__:
                    self.rfid_buffer.append(chr(char_buf[0]))
                else:
                    card_id = self.incoming_data_read()
                    self.process_card_id(card_id)
            if not self.in_queue.empty():
                control_event = self.in_queue.get(block=False)
                self.process_control_event(control_event)

        self.mcu.close()
        self.rfid.close()


class Manager():
    def __init__(self, url):
        self.stop_event = threading.Event()
        self.to_serial = queue.Queue()
        self.from_serial = queue.Queue()
        self.serial_manager = SerialManager("/dev/ttyACM0", 9600, "/dev/ttyUSB0", 9600,
                                            self.stop_event,
                                            self.to_serial, self.from_serial)
        self.server = websocket.WebSocketApp(url)
        self.server.run_forever(sslopt={"cert_reqs": websocket.ssl.CERT_NONE})
        self.server.send("asd".encode(encoding='UTF-8', errors='strict'))

    HOSTNAME = '10.255.5.43'    # The remote host
    PORT = 8080              # The same port as used by the server

    def handshake(host, port):
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

man = Manager("http://10.255.5.43:8080")

