from pynput import mouse
import threading
import time
import pyautogui 

class MouseRecorder:
    def __init__(self):
        self.events = []
        self.screen_width, self.screen_height = pyautogui.size()  # Get screen dimensions
        self.listener = None

    def on_move(self, x, y):
        # Normalize coordinates
        normalized_x = x / self.screen_width
        normalized_y = y / self.screen_height
        self.events.append(("move", normalized_x, normalized_y, time.time()))

    def on_click(self, x, y, button, pressed):
        normalized_x = x / self.screen_width
        normalized_y = y / self.screen_height
        action = "press" if pressed else "release"
        self.events.append((action, normalized_x, normalized_y, button.name, time.time()))

    def start_recording(self):
        self.events.clear()
        self.listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        self.listener.start()

    def stop_recording(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

    def save_recording(self, filename="mouse_events.txt"):
        with open(filename, "w") as file:
            for event in self.events:
                file.write(f"{event}\n")