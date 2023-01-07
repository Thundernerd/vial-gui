import json
import time
import sys
import pywinctl as pwc
import pythoncom
from multiprocessing import RLock

from PyQt5.QtCore import pyqtSignal, QThread

class ProfileSwitcherThread(QThread):

    window_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.active_window = None
        self.locked = False
        self.mutex = RLock()

    def run(self):
        pythoncom.CoInitialize()
        while True:
            self.update()
            time.sleep(1)

    def lock(self):
        with self.mutex:
            self.locked = True

    def unlock(self):
        with self.mutex:
            self.locked = False

    def update(self):
        # if lock()ed then just do nothing
        with self.mutex:
            if self.locked:
                return

            wnd = pwc.getActiveWindow()
            if wnd is None:
                return

            try:
                current_window = wnd.getAppName()
            except:
                print("cannot get current window for some reason")
                return

            if current_window != self.active_window:
                self.active_window = current_window
                self.window_updated.emit(current_window)
