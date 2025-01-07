from pynput.mouse import Controller, Button
import time
import pyautogui  # For screen dimensions
import ast

class MousePlayback:
    def __init__(self, speed=1):
        self.mouse = Controller()
        self.speed = speed
        self.events = []
        self.screen_width, self.screen_height = pyautogui.size()

    def load_events(self, filename="mouse_events.txt"):
        try:
            with open(filename, "r") as file:
                self.events = [ast.literal_eval(line.strip()) for line in file]
        except Exception as e:
            raise ValueError(f"Error loading events: {e}")

    def play_events(self, repeat=1):
        if not self.events:
            raise ValueError("No events loaded. Please load events first.")

        for _ in range(repeat):
            start_time = self.events[0][-1]
            for event in self.events:
                if not isinstance(event, tuple) or len(event) < 4:
                    print(f"Skipping invalid event: {event}")
                    continue

                action, *details, event_time = event
                delay = (event_time - start_time) / self.speed
                time.sleep(delay)
                start_time = event_time

                if action == "move":
                    normalized_x, normalized_y = details
                    x = int(normalized_x * self.screen_width)
                    y = int(normalized_y * self.screen_height)
                    self.mouse.position = (x, y)
                elif action in ["press", "release"]:
                    normalized_x, normalized_y, button = details
                    x = int(normalized_x * self.screen_width)
                    y = int(normalized_y * self.screen_height)
                    btn = Button.left if button == "left" else Button.right
                    self.mouse.position = (x, y)
                    if action == "press":
                        self.mouse.press(btn)
                    else:
                        self.mouse.release(btn)