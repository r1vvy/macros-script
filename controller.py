import keyboard
import time
import threading
from config import Config

class MacroController:
    def __init__(self, config: Config):
        self.config = config
        self.run_macro = False
        self.macro_thread = None
        self.thread_lock = threading.Lock()
        self.update_key_bindings()

    def macro_loop(self):
        while self.run_macro:
            if self.config.macro_key:
                keyboard.release(self.config.macro_key)
                time.sleep(self.config.sleep_time)
                keyboard.press(self.config.macro_key)
                time.sleep(self.config.sleep_time)
            else:
                break

    def start_macro(self, e=None):
        with self.thread_lock:
            if not self.run_macro and self.config.macro_key is not None:
                self.run_macro = True
                print("Starting macro...")
                if self.macro_thread is None or not self.macro_thread.is_alive():
                    self.macro_thread = threading.Thread(target=self.macro_loop, daemon=True)
                    self.macro_thread.start()

    def stop_macro(self, e=None):
        with self.thread_lock:
            if self.run_macro:
                print("Stopping macro...")
                self.run_macro = False
                if self.macro_thread is not None:
                    self.macro_thread.join(timeout=0.05)
                    self.macro_thread = None

    def toggle_macro(self):
        if self.config.macro_key is not None:
            self.stop_macro()
            self.config.macro_key = None
            print("Macro key disabled.")
        else:
            self.config.macro_key = self.config.saved_macro_key
            print("Macro key enabled.")

    def apply_settings(self, new_macro_key, new_toggle_key, new_sleep_time):
        self.config.macro_key = new_macro_key
        self.config.saved_macro_key = new_macro_key
        self.config.toggle_key = new_toggle_key
        self.config.sleep_time = new_sleep_time
        self.update_key_bindings()
        # Restart macro with new settings if needed
        if self.run_macro:
            self.stop_macro()
            self.start_macro()

    def update_key_bindings(self):
        keyboard.unhook_all()
        if self.config.macro_key is not None:
            keyboard.on_press_key(self.config.macro_key, self.start_macro)
            keyboard.on_release_key(self.config.macro_key, self.stop_macro)
        keyboard.add_hotkey(self.config.toggle_key, self.toggle_macro)
