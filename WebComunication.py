__author__ = 'kalo'
import threading
import time


class WebComunication(threading.Thread):
    def __init__(self, in_queue, out_queue, stop_event):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.stop_event = stop_event
        self.card_map_dict = {"6A003E858253": "obbo1", "67007BBBEB4C": "obbb2", "6A003E6BA09F": "oobo3"}

    def run(self):
        while not self.stop_event.is_set():
            if not self.in_queue.empty():
                data = self.in_queue.get(block=False)
                print(str(data[1]))  # at game start prints card id, at end prints time
                if data[0] == "getPattern":
                    self.out_queue.put(self.card_map_dict[data[1]])

            time.sleep(0.001)