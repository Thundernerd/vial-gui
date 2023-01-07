import sys

from profileswitcher.profileswitcher_thread import ProfileSwitcherThread

from PyQt5.QtCore import QObject, pyqtSignal

class ProfileSwitcher(QObject):
    window_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.thread = ProfileSwitcherThread()
        self.thread.window_updated.connect(self.on_window_updated)
        self.thread.start()

    def _lock(self):
        self.thread.lock()

    def _unlock(self):
        self.thread.unlock()

    def on_window_updated(self, active_window):
        self.active_window = active_window
        self.window_updated.emit(active_window)