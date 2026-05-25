import keyboard
import threading

class HotkeyManager:
    def __init__(self, combo, callback):
        self.combo = combo
        self.callback = callback
        self.lock = threading.Lock()
        self.processing = False

    def handler(self):
        with self.lock:
            if not self.processing:
                self.processing = True
                try:
                    self.callback()
                finally:
                    self.processing = False

    def start(self):
        keyboard.add_hotkey(self.combo, self.handler)
        print(f"⌨️  Горячая клавиша {self.combo} зарегистрирована.")