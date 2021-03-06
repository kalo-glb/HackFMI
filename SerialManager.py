__author__ = 'kalo'
from Events import Events, EventTypes
import threading
import serial
import time


class SerialManager(threading.Thread):
    __msg_start_char__ = '\x02'
    __msg_end_char__ = b'\x03'
    __msg_len = 15

    def __init__(self, mcu_serial_port, mcu_baud_rate, rfid_port, rfid_baud_rate, stop_event, in_queue, out_queue):
        threading.Thread.__init__(self)
        self.mcu = serial.Serial(mcu_serial_port, mcu_baud_rate)
        self.rfid = serial.Serial(rfid_port, rfid_baud_rate)
        self.rfid_buffer = list()
        self.stop_event = stop_event
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.end_sent = False

    def set_sensor_pattern(self, pattern):
        self.end_sent = False
        self.mcu.write(pattern)

    def incoming_data_read(self):
        card_id = ""
        for cnt in range(self.__msg_len):
            char = self.rfid_buffer.pop()
            if char == self.__msg_start_char__:
                self.rfid_buffer = list()
                break
            if char == '\r' or char == '\n':
                continue

            card_id += str(char)

        card_id = card_id[::-1]

        return card_id

    def write_to_manager(self, event_type, e, data=None):
        if data is None:
            msg = {"event_type": event_type, "e": e}
        else:
            msg = {"event_type": event_type, "e": e}

        self.out_queue.put(msg)

    def process_card_id(self, card_id):
        self.write_to_manager(EventTypes.rfid_event, card_id)

    def process_mcu_event(self, event):
        e = Events.error
        if 'e' == event:
            e = Events.player_error
        elif '1' == event:
            e = Events.player_start_labirinth
        elif '4' == event and self.end_sent is False:
            self.end_sent = True
            e = Events.player_won

        self.write_to_manager(EventTypes.mcu_event, e)

    def process_control_event(self, event):
        self.set_sensor_pattern(event)

    def run(self):
        while not self.stop_event.is_set():
            if self.mcu.inWaiting():
                e = self.mcu.read()
                self.process_mcu_event(e)
            if not self.in_queue.empty():
                self.process_control_event(self.in_queue.get())
            if self.rfid.inWaiting():
                char_buf = self.rfid.read()
                if char_buf != self.__msg_end_char__:
                    self.rfid_buffer.append(char_buf[0])
                else:
                    card_id = self.incoming_data_read()
                    self.process_card_id(card_id)
            if not self.in_queue.empty():
                control_event = self.in_queue.get(block=False)
                self.process_control_event(control_event)

            time.sleep(0.01)

        self.mcu.close()
        self.rfid.close()