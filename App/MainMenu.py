import tkinter as tk
from PIL import Image, ImageTk
import sys


class MainMenu(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_widgets()

    def load_image(self):
        self.background_image = Image.open('assets/BgHome.png')
        self.play_btn_image = Image.open('assets/button/Button Mulai.png')
        self.hover_play_btn_image = Image.open(
            'assets/button/Button Mulai Hover.png')
        self.about_btn_image = Image.open('assets/button/Button Tentang.png')
        self.hover_about_btn_image = Image.open(
            'assets/button/Button Tentang Hover.png')
        self.quit_btn_image = Image.open('assets/button/Button Keluar.png')
        self.hover_quit_btn_image = Image.open(
            'assets/button/Button Keluar Hover.png')

        # Convert images to Tkinter PhotoImage objects
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.play_btn_photo = ImageTk.PhotoImage(self.play_btn_image)
        self.hover_play_btn_photo = ImageTk.PhotoImage(
            self.hover_play_btn_image)
        self.about_btn_photo = ImageTk.PhotoImage(self.about_btn_image)
        self.hover_about_btn_photo = ImageTk.PhotoImage(
            self.hover_about_btn_image)
        self.quit_btn_photo = ImageTk.PhotoImage(self.quit_btn_image)
        self.hover_quit_btn_photo = ImageTk.PhotoImage(
            self.hover_quit_btn_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.menu_manager.screen_width, height=self.menu_manager.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)

    def create_widgets(self):
        play_btn = tk.Button(
            self.background_canvas, image=self.play_btn_photo, command=self.show_play_menu, borderwidth=0)
        play_btn.place(x=822, y=357)
        play_btn.bind('<Enter>', lambda event: play_btn.config(
            image=self.hover_play_btn_photo))
        play_btn.bind('<Leave>', lambda event: play_btn.config(
            image=self.play_btn_photo))

        about_btn = tk.Button(
            self.background_canvas, image=self.about_btn_photo, command=self.show_about_menu, borderwidth=0)
        about_btn.place(x=822, y=465)
        about_btn.bind('<Enter>', lambda event: about_btn.config(
            image=self.hover_about_btn_photo))
        about_btn.bind('<Leave>', lambda event: about_btn.config(
            image=self.about_btn_photo))

        quit_btn = tk.Button(
            self.background_canvas, image=self.quit_btn_photo, command=self.show_quit_menu, borderwidth=0)
        quit_btn.place(x=822, y=573)
        quit_btn.bind('<Enter>', lambda event: quit_btn.config(
            image=self.hover_quit_btn_photo))
        quit_btn.bind('<Leave>', lambda event: quit_btn.config(
            image=self.quit_btn_photo))

    def show_play_menu(self):
        self.menu_manager.show_menu("play")

    def show_about_menu(self):
        self.menu_manager.show_menu("about")

    def show_quit_menu(self):
        sys.exit()
