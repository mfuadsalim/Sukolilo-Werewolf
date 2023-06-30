import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from App.Night import Night


class WelcomeGame(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_widgets()
        self.start_timer(10)


    def load_image(self):
        self.background_image = Image.open('assets/BgWelcome.png')

        self.background_photo = ImageTk.PhotoImage(self.background_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.menu_manager.screen_width, height=self.menu_manager.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)

    def create_widgets(self):
        player_name = tk.Label(self.background_canvas, text=self.menu_manager.name, background='#ECE3D5' ,
                               font=('Arial', 12))
        player_name.place(x=665, y=195)

        role = self.menu_manager.role

        role_card_path = 'assets/RoleCard' + role + '.png'
        self.role_card_image = Image.open(role_card_path)
        self.role_card_photo = ImageTk.PhotoImage(self.role_card_image)
        role_card = tk.Label(self.background_canvas, image=self.role_card_photo, background='#ECE3D5')
        role_card.place(x=286, y=326)

        role_desc_path = 'assets/RoleDesc' + role + '.png'
        self.role_desc_image = Image.open(role_desc_path)
        self.role_desc_photo = ImageTk.PhotoImage(self.role_desc_image)
        role_desc = tk.Label(self.background_canvas, image=self.role_desc_photo, background='#ECE3D5')
        role_desc.place(x=528, y=332)

        self.timer_label = tk.Label(self.background_canvas, text='', foreground='#ECE3D5', background="#612C12", font=('Arial', 32))
        self.timer_label.place(x=1015, y=585)

    def start_timer(self, seconds):
        self.remaining_time = seconds
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.configure(text=self.remaining_time)
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            self.menu_manager.menus["night"] = Night(
                self.menu_manager, self.menu_manager)
            self.menu_manager.show_menu("night")

