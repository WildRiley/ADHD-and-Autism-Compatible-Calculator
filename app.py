import tkinter as tk
import pygame as py
import time
import os
import sys


def resource_path(relative_path):
    """i dont hate pyinstaller haha"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Calculator:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.initialize_sounds()
        self.create_widgets()
        self.text_result = "0"

    def setup_window(self):
        """it prepares the window :0"""
        self.master.title("ADHD & Autism Compatible Calculator")
        self.master.resizable(False, False)
        self.master.geometry("400x610")
        self.master.configure(bg="mediumpurple2")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.iconbitmap(resource_path("sfx/epicLogo.ico"))

        # Background music
        py.mixer.init()
        py.mixer.music.load(resource_path("sfx/bg music.mp3"))
        py.mixer.music.play(-1)

    def initialize_sounds(self):
        """it loads sounds :0"""
        self.sounds = {
            "button_press": py.mixer.Sound(resource_path("sfx/buttonPress.mp3")),
            "explosion": py.mixer.Sound(resource_path("sfx/explosion.mp3")),
            "correct": py.mixer.Sound(resource_path("sfx/correctSfx.mp3")),
            "incorrect": py.mixer.Sound(resource_path("sfx/incorrectSfx.mp3")),
            "delete": py.mixer.Sound(resource_path("sfx/delete.mp3")),
            "closing": py.mixer.Sound(resource_path("sfx/closing.mp3")),
        }

    def create_widgets(self):
        """widget creation or something :0"""
        # Display
        self.result = tk.Label(
            self.master, text="0", font=("bahnschrift", 24), anchor="e",
            bg="white", relief="sunken"
        )
        self.result.pack(padx=10, pady=10, fill="x")

        # Grid
        button_frame = tk.Frame(self.master, bg="mediumpurple2")
        button_frame.pack(pady=20)

        button_specs = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2),
            ("0", 3, 1), ("+", 4, 0), ("-", 4, 1),
            ("*", 4, 2), ("/", 5, 0), ("=", 5, 1),
            ("Clear", 6, 0), ("Backspace", 6, 2)
        ]

        for text, row, col in button_specs:
            self.create_button(button_frame, text, row, col)

        # Special buttons
        self.btn_music = tk.Button(
            button_frame, text="Toggle Music", font=("TkDefaultFont", 7),
            width=9, height=2, bg='orange', command=self.toggle_music
        )
        self.btn_music.grid(row=7, column=2, columnspan=1, padx=5, pady=5, sticky="se")

        self.watermark = tk.Label(
            button_frame, text="Made by RileyIsPurple!",
            font=("TkDefaultFont", 8), bg="mediumpurple2"
        )
        self.watermark.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="sw")

    def create_button(self, frame, text, row, col):
        """button creation :0"""
        command = self.get_command(text)
        bg_color = "chocolate1" if text.isdigit() else "red" if text == "Clear" else "firebrick3"
        btn = tk.Button(
            frame, text=text, width=8, height=3, bg=bg_color,
            command=command
        )
        btn.grid(row=row, column=col, padx=5, pady=5)

    def get_command(self, text):
        """it returns stuff :0"""
        if text.isdigit():
            return lambda: self.number(text)
        elif text in "+-*/":
            return lambda: self.number(text)
        elif text == "=":
            return self.calculate
        elif text == "Clear":
            return self.clear
        elif text == "Backspace":
            return self.remove_number

    def play_sound(self, sound_name):
        """it plays sound :0"""
        py.mixer.Sound.play(self.sounds[sound_name])

    def number(self, value):
        self.play_sound("button_press")
        self.text_result = value if self.text_result == "0" else self.text_result + value
        self.result.config(text=self.text_result)

    def remove_number(self):
        self.play_sound("delete")
        self.text_result = self.text_result[:-1] or "0"
        self.result.config(text=self.text_result)

    def on_closing(self):
        self.play_sound("closing")
        py.mixer.music.stop()
        time.sleep(2)
        self.master.destroy()

    def calculate(self):
        try:
            self.text_result = str(eval(self.text_result))
            self.play_sound("correct")
        except Exception:
            self.play_sound("incorrect")
            self.text_result = "Error"
        self.result.config(text=self.text_result)

    def clear(self):
        self.play_sound("explosion")
        self.text_result = "0"
        self.result.config(text=self.text_result)

    def toggle_music(self):
        if py.mixer.music.get_busy():
            py.mixer.music.stop()
        else:
            py.mixer.music.play(-1)


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()