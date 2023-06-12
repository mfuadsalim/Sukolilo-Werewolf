import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MainMenu(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_widgets()

    def load_image(self):
        self.background_photo = tk.PhotoImage(file='assets/Background.png')
        self.team_photo = tk.PhotoImage(file='assets/By Kelompok 1.png')
        self.title_photo = tk.PhotoImage(file='assets/Title.png')
        self.create_room_btn_photo = tk.PhotoImage(file='assets/Button Create Room.png')
        self.join_room_btn_photo = tk.PhotoImage(file='assets/Button Join Room.png')

    def create_canvas(self):
        self.background_canvas = tk.Canvas(self, width=1920, height=1080)
        self.background_canvas.pack()
        self.background_canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)
        self.background_canvas.create_image(50, 50, anchor=tk.NW, image=self.team_photo)
        self.background_canvas.create_image(850, 50, anchor=tk.NW, image=self.title_photo)

    def create_widgets(self):
        create_button = ttk.Button(self.background_canvas, image=self.create_room_btn_photo, command=self.show_create_menu)
        create_button.place(x=1100, y=450)

        join_button = ttk.Button(self.background_canvas, image=self.join_room_btn_photo, command=self.show_join_menu)
        join_button.place(x=1100, y=600)

    def show_create_menu(self):
        self.menu_manager.show_menu("create")

    def show_join_menu(self):
        self.menu_manager.show_menu("join")

    def show_how_to_play_menu(self):
        self.menu_manager.show_menu("how_to_play")