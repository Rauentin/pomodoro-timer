# simple tkinter gui

import tkinter as tk
from tkinter import ttk
from pathlib import Path
import pygame
from timer import PomodoroTimer

SOUNDS = Path(__file__).parent / "sounds"

BG, CARD, FG = "#1e222a", "#2c313c", "#e6e6e6"
MUTED, WORK, BREAK = "#8b93a1", "#e06c75", "#98c379"


class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # Audio is optional: on a machine with no sound device the timer still runs.
        try:
            pygame.mixer.init()
            self.audio = True
        except pygame.error as e:
            print(f"Sound disabled: {e}")
            self.audio = False

        self.timer = PomodoroTimer()

        self._init_style()
        main = ttk.Frame(root, padding=28)
        main.grid()

        # Time display + status
        self.time_label = ttk.Label(main, text="25:00", font=("Segoe UI Light", 56))
        self.time_label.grid(row=0, column=0, columnspan=3)
        self.status_label = ttk.Label(main, text="Work", font=("Segoe UI", 12))
        self.status_label.grid(row=1, column=0, columnspan=3, pady=(0, 22))

        # Work/Break length inputs
        inputs = ttk.Frame(main)
        inputs.grid(row=2, column=0, columnspan=3, pady=(0, 18))
        self.work_var = tk.IntVar(value=25)
        self.break_var = tk.IntVar(value=5)
        for col, (text, var) in enumerate((("Work", self.work_var), ("Break", self.break_var))):
            ttk.Label(inputs, text=text, style="Muted.TLabel").grid(row=0, column=col * 2, padx=(0, 6))
            ttk.Spinbox(inputs, from_=1, to=180, width=4, textvariable=var,
                        justify="center").grid(row=0, column=col * 2 + 1, padx=(0, 18))

        # Buttons
        ttk.Button(main, text="Start", command=self.start).grid(row=3, column=0, padx=4)
        self.pause_btn = ttk.Button(main, text="Pause", command=self.toggle_pause)
        self.pause_btn.grid(row=3, column=1, padx=4)
        ttk.Button(main, text="Reset", command=self.reset).grid(row=3, column=2, padx=4)

        self.refresh()
        self.run_timer()

    def _init_style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TFrame", background=BG)
        s.configure("TLabel", background=BG, foreground=FG)
        s.configure("Muted.TLabel", foreground=MUTED, font=("Segoe UI", 9))
        s.configure("TButton", background=CARD, foreground=FG, borderwidth=0,
                    padding=(16, 8), font=("Segoe UI", 10))
        s.map("TButton", background=[("active", "#3a4150")])
        s.configure("TSpinbox", fieldbackground=CARD, background=CARD, foreground=FG,
                    borderwidth=0, arrowsize=11, insertcolor=FG)

    def minutes(self, var, default):
        """Read a spinbox value, falling back to default if it's been cleared."""
        try:
            return max(1, var.get()) * 60
        except tk.TclError:
            return default * 60

    def start(self):
        self.timer.work_time = self.minutes(self.work_var, 25)
        self.timer.break_time = self.minutes(self.break_var, 5)
        self.timer.running = True
        self.refresh()

    def toggle_pause(self):
        self.timer.toggle_pause()
        self.refresh()

    def reset(self):
        self.timer.reset()
        self.timer.time_left = self.minutes(self.work_var, 25)
        self.refresh()

    def refresh(self):
        """Sync the display, status text and pause button with the timer state."""
        self.time_label.config(text=self.timer.get_time_display())
        working = self.timer.is_work
        self.status_label.config(text="Work" if working else "Break",
                                 foreground=WORK if working else BREAK)
        self.pause_btn.config(text="Pause" if self.timer.running else "Resume")

    def play_sound(self, filename):
        if not self.audio:
            return
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
        except Exception:
            print(f"Could not play {filename}")

    def run_timer(self):
        period = self.timer.tick()
        if period:  # a period just ended
            self.play_sound(SOUNDS / ("start.wav" if period == "work" else "break.wav"))
        self.refresh()
        self.root.after(1000, self.run_timer)  # run every second


if __name__ == "__main__":
    root = tk.Tk()
    PomodoroApp(root)
    root.mainloop()
