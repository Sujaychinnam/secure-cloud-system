import time
import threading
import os


class FileSync:

    def __init__(self,callback):

        self.callback = callback

        self.running = False

        self.last_state = set()

    # ==========================================

    def start(self):

        self.running = True

        thread = threading.Thread(target=self.watch)

        thread.daemon = True

        thread.start()

    # ==========================================

    def watch(self):

        while self.running:

            if os.path.exists("storage"):

                files = set(os.listdir("storage"))

                new_files = files - self.last_state

                if new_files:

                    for f in new_files:

                        self.callback(f)

                self.last_state = files

            time.sleep(5)