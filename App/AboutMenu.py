import tkinter as tk
from PIL import Image, ImageTk


class AboutMenu(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_widgets()

    def load_image(self):
        self.background_image = Image.open('assets/BgAbout.png')
        self.back_btn_image = Image.open('assets/button/Button Kembali.png')
        self.hover_back_btn_image = Image.open(
            'assets/button/Button Kembali Hover.png')

        # Convert images to Tkinter PhotoImage objects
        self.background_photo = ImageTk.PhotoImage(self.background_image)
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
        back_button = tk.Button(
            self, image=self.back_btn_photo, command=self.menu_manager.show_main_menu, borderwidth=0)
        back_button.place(x=528, y=604)
        back_button.bind('<Enter>', lambda event: back_button.config(
            image=self.hover_back_btn_photo))
        back_button.bind('<Leave>', lambda event: back_button.config(
            image=self.back_btn_photo))
