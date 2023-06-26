import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import ctypes

class MainMenu(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_widgets()

    def load_image(self):
        self.background_image = Image.open('assets/Background.png')
        self.team_image = Image.open('assets/By Kelompok 1.png')
        self.title_image = Image.open('assets/Title.png')
        self.create_room_btn_image = Image.open('assets/Button Create Room.png')
        self.join_room_btn_image = Image.open('assets/Button Join Room.png')

        # Get screen resolution
        user32 = ctypes.windll.user32
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)

        # Resize images based on screen resolution
        self.background_image = self.background_image.resize((self.screen_width, self.screen_height), Image.ANTIALIAS)
        self.team_image = self.team_image.resize((int(self.screen_width / 6), int(self.screen_height / 9)), Image.ANTIALIAS)
        self.title_image = self.title_image.resize((int(self.screen_width / 2), int(self.screen_height / 3)), Image.ANTIALIAS)
        self.create_room_btn_image = self.create_room_btn_image.resize((int(self.screen_width / 5), int(self.screen_height / 8)), Image.ANTIALIAS)
        self.join_room_btn_image = self.join_room_btn_image.resize((int(self.screen_width / 5), int(self.screen_height / 8)), Image.ANTIALIAS)

        # Convert images to Tkinter PhotoImage objects
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.team_photo = ImageTk.PhotoImage(self.team_image)
        self.title_photo = ImageTk.PhotoImage(self.title_image)
        self.create_room_btn_photo = ImageTk.PhotoImage(self.create_room_btn_image)
        self.join_room_btn_photo = ImageTk.PhotoImage(self.join_room_btn_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)
        self.background_canvas.create_image(int(self.screen_width / 100), int(self.screen_height / 100), anchor=tk.NW, image=self.team_photo)
        self.background_canvas.create_image(int(self.screen_width * 0.55) - int(self.screen_width / 8), int(self.screen_height / 12), anchor=tk.NW, image=self.title_photo)


    def create_widgets(self):
        create_button = ttk.Button(self.background_canvas, image=self.create_room_btn_photo, command=self.show_create_menu)
        create_button.place(x=int(self.screen_width / 1.6), y=int(self.screen_height / 2.5))

        join_button = ttk.Button(self.background_canvas, image=self.join_room_btn_photo, command=self.show_join_menu)
        join_button.place(x=int(self.screen_width / 1.6), y=int(self.screen_height / 1.8))

    def show_create_menu(self):
        self.menu_manager.show_menu("create")

    def show_join_menu(self):
        self.menu_manager.show_menu("join")

    def show_how_to_play_menu(self):
        self.menu_manager.show_menu("how_to_play")
