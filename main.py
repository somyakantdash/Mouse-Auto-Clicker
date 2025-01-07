import tkinter as tk
import threading
from recorder import MouseRecorder
from playback import MousePlayback

def start_recording():
    def record():
        recorder.start_recording()
        status_label.config(text="Recording...")
    threading.Thread(target=record, daemon=True).start()

def stop_and_save():
    recorder.stop_recording()
    recorder.save_recording()
    status_label.config(text="Recording saved!")

def play_recording():
    try:
        # Validate repeat input
        repeat_text = repeat_entry.get()
        if not repeat_text.strip().isdigit():
            status_label.config(text="Invalid repeat value. Using default: 1.")
            repeat = 1
        else:
            repeat = int(repeat_text)

        # Validate speed input
        speed_text = speed_var.get()
        if not speed_text.strip().isdigit() or int(speed_text) not in [1, 2, 4, 8]:
            status_label.config(text="Invalid speed value. Using default: 1x.")
            speed = 1
        else:
            speed = int(speed_text)

        playback.load_events()  # Ensure events are loaded
        playback.speed = speed
        playback.play_events(repeat)
        status_label.config(text="Playback completed!")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

# Initialize recorder and playback
recorder = MouseRecorder()
playback = MousePlayback()

# GUI
root = tk.Tk()
root.title("Mouse Recorder")
root.geometry("400x300")
root.attributes('-topmost', True)

start_btn = tk.Button(root, text="Start Recording", command=start_recording)
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="Stop & Save", command=stop_and_save)
stop_btn.pack(pady=10)

play_btn = tk.Button(root, text="Play Recording", command=play_recording)
play_btn.pack(pady=10)

repeat_label = tk.Label(root, text="Repeat Times:")
repeat_label.pack()
repeat_entry = tk.Entry(root)
repeat_entry.pack()

speed_label = tk.Label(root, text="Speed (1x-8x):")
speed_label.pack()
speed_var = tk.StringVar(value="1")
speed_entry = tk.OptionMenu(root, speed_var, *["1", "2", "4", "8"])
speed_entry.pack()

status_label = tk.Label(root, text="Status: Idle")
status_label.pack(pady=10)

root.mainloop()
