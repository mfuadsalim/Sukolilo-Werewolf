import tkinter as tk
from PIL import Image, ImageTk
import pickle
import threading
import time

class Chat(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        # self.create_widgets()

        # self.chat_thread = threading.Thread(target=self.update)
        # self.is_running = True
        # # Set the thread as a daemon to stop it when the main thread exits
        # self.chat_thread.daemon = True
        # self.chat_thread.start()

        # self.start_timer(8)

    def load_image(self):
        self.background_image = Image.open('assets/BgSiang.png')

        self.background_photo = ImageTk.PhotoImage(self.background_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.menu_manager.screen_width, height=self.menu_manager.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)
