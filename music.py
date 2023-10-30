import tkinter as tk
from tkinter import filedialog
from pygame import mixer  # You need to install the pygame library: pip install pygame

mixer.init()

# Function to open a file dialog and select a music file to play
def play_music():
    file_path = filedialog.askopenfilename(filetypes=[("Music files", "*.mp3")])
    if file_path:
        mixer.music.load(file_path)
        mixer.music.play()

# Function to stop the currently playing music
def stop_music():
    mixer.music.stop()
