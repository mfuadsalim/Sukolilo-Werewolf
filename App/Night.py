import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk



class Night(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_widgets()
        self.start_timer(20)

    def load_image(self):
        self.background_image = Image.open('assets/BgMalam.png')
        self.do_btn_image = Image.open('assets/button/Small Button Lakukan.png')
        self.hover_do_btn_image = Image.open('assets/button/Small Button Lakukan Hover.png')
        self.text_malam_1_image = Image.open('assets/TextMalam1.png')
        self.text_malam_2_image = Image.open('assets/TextMalam2.png')

        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.do_btn_photo = ImageTk.PhotoImage(self.do_btn_image)
        self.hover_do_btn_photo = ImageTk.PhotoImage(self.hover_do_btn_image)
        self.text_malam_1_photo = ImageTk.PhotoImage(self.text_malam_1_image)
        self.text_malam_2_photo = ImageTk.PhotoImage(self.text_malam_2_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.menu_manager.screen_width, height=self.menu_manager.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)

    def create_widgets(self):
        role = self.menu_manager.role
        action = self.menu_manager.action

        role_card_path = 'assets/RoleCard' + role + '.png'
        self.role_card_image = Image.open(role_card_path)
        self.role_card_photo = ImageTk.PhotoImage(self.role_card_image)
        role_card = tk.Label(self.background_canvas, image=self.role_card_photo, background='#ECE3D5')

        if role == "Mahasiswa":
            text_malam = tk.Label(self.background_canvas, image=self.text_malam_2_photo, background='#ECE3D5')
            role_card.place(x=540, y=282)
        else:
            text_malam = tk.Label(self.background_canvas, image=self.text_malam_1_photo, background='#ECE3D5')
            role_card.place(x=344, y=282)

        text_malam.place(x=312, y=183)

        self.timer_label = tk.Label(self.background_canvas, text='', foreground='#ECE3D5', background="#612C12",
                                    font=('Arial', 32))
        self.timer_label.place(x=958, y=557)

    def start_timer(self, seconds):
        self.remaining_time = seconds
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.configure(text=self.remaining_time)
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            pass

