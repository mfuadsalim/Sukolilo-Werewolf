import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import ctypes


class PlayMenu(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_widgets()

    def load_image(self):
        self.background_image = Image.open('assets/BgHome.png')
        self.create_room_btn_image = Image.open(
            'assets/button/Button Buat.png')
        self.hover_create_room_btn_image = Image.open(
            'assets/button/Button Buat Hover.png')
        self.join_room_btn_image = Image.open(
            'assets/button/Button Gabung.png')
        self.hover_join_room_btn_image = Image.open(
            'assets/button/Button Gabung Hover.png')
        self.back_btn_image = Image.open('assets/button/Button Kembali.png')
        self.hover_back_btn_image = Image.open(
            'assets/button/Button Kembali Hover.png')

        # Convert images to Tkinter PhotoImage objects
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.create_room_btn_photo = ImageTk.PhotoImage(
            self.create_room_btn_image)
        self.hover_create_room_btn_photo = ImageTk.PhotoImage(
            self.hover_create_room_btn_image)
        self.join_room_btn_photo = ImageTk.PhotoImage(self.join_room_btn_image)
        self.hover_join_room_btn_photo = ImageTk.PhotoImage(
            self.hover_join_room_btn_image)
        self.back_btn_photo = ImageTk.PhotoImage(self.back_btn_image)
        self.hover_back_btn_photo = ImageTk.PhotoImage(
            self.hover_back_btn_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.menu_manager.screen_width, height=self.menu_manager.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)

    def create_widgets(self):
        create_room_btn = tk.Button(
            self.background_canvas, image=self.create_room_btn_photo, command=self.show_create_menu, borderwidth=0)
        create_room_btn.place(x=922, y=357)
        create_room_btn.bind('<Enter>', lambda event: create_room_btn.config(
            image=self.hover_create_room_btn_photo))
        create_room_btn.bind('<Leave>', lambda event: create_room_btn.config(
            image=self.create_room_btn_photo))

        join_room_btn = tk.Button(
            self.background_canvas, image=self.join_room_btn_photo, command=self.show_join_menu, borderwidth=0)
        join_room_btn.place(x=822, y=465)
        join_room_btn.bind('<Enter>', lambda event: join_room_btn.config(
            image=self.hover_join_room_btn_photo))
        join_room_btn.bind('<Leave>', lambda event: join_room_btn.config(
            image=self.join_room_btn_photo))

        quit_btn = tk.Button(
            self.background_canvas, image=self.back_btn_photo, command=self.menu_manager.show_main_menu, borderwidth=0)
        quit_btn.place(x=722, y=573)
        quit_btn.bind('<Enter>', lambda event: quit_btn.config(
            image=self.hover_back_btn_photo))
        quit_btn.bind('<Leave>', lambda event: quit_btn.config(
            image=self.back_btn_photo))

    def show_create_menu(self):
        self.menu_manager.show_menu("create")

    def show_join_menu(self):
        self.menu_manager.show_menu("join")
