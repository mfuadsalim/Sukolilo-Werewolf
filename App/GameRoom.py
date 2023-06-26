import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class GameRoom(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        # self.create_canvas()
        self.create_widgets()

    def load_image(self):
        self.background_photo = tk.PhotoImage(file='assets/Game Room Background.png')

    def create_canvas(self):
        self.background_canvas = tk.Canvas(self, width=1920, height=1080)
        self.background_canvas.pack()
        self.background_canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)

    def create_widgets(self):
        back_button = ttk.Button(self, text="Back to Menu", command=self.menu_manager.show_main_menu)
        back_button.pack()

        # create_button = ttk.Button(self.background_canvas, image=self.create_room_btn_photo, command=self.show_create_menu)
        # create_button.place(x=1100, y=450)

        # join_button = ttk.Button(self.background_canvas, image=self.join_room_btn_photo, command=self.show_join_menu)
        # join_button.place(x=1100, y=600)

    # def show_create_menu(self):
    #     self.menu_manager.show_menu("create")

    # def show_join_menu(self):
    #     self.menu_manager.show_menu("join")

    # def show_how_to_play_menu(self):
    #     self.menu_manager.show_menu("how_to_play")