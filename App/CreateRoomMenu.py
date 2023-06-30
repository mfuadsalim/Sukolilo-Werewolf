import tkinter as tk
from tkinter import ttk
import pickle
import random
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox

from App.WaitingRoom import WaitingRoom


class CreateRoomMenu(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_widgets()

    def load_image(self):
        self.background_image = Image.open(
            'assets/BgBuat.png')
        self.create_btn_image = Image.open(
            'assets/button/Small Button Buat.png')
        self.hover_create_btn_image = Image.open(
            'assets/button/Small Button Buat Hover.png')
        self.back_btn_image = Image.open(
            'assets/button/Small Button Kembali.png')
        self.hover_back_btn_image = Image.open(
            'assets/button/Small Button Kembali Hover.png')

        # Convert images to Tkinter PhotoImage objects
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.create_btn_photo = ImageTk.PhotoImage(self.create_btn_image)
        self.hover_create_btn_photo = ImageTk.PhotoImage(
            self.hover_create_btn_image)
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
        # Create input field
        self.name_entry = ttk.Entry(
            self.background_canvas, width=40, background="#ECE3D5")
        self.name_entry.place(x=520, y=279)
        self.placeholder_text = "Masukkan nama anda..."
        self.name_entry.insert(0, self.placeholder_text)
        self.name_entry.configure(foreground="gray")
        self.name_entry.bind('<FocusIn>', self.on_entry_click)

        self.player_var = ttk.Entry(
            self.background_canvas, width=40, background='#ECE3D5')
        self.player_var = tk.StringVar(self)
        self.player_var.set("4")
        player_dropdown = ttk.OptionMenu(
            self, self.player_var, self.player_var.get(), "4", "8", "12")
        player_dropdown.place(x=620, y=408)

        create_button = tk.Button(
            self.background_canvas, image=self.create_btn_photo, command=self.create_room, borderwidth=0)
        create_button.place(x=563, y=490)
        create_button.bind('<Enter>', lambda event: create_button.config(
            image=self.hover_create_btn_photo))
        create_button.bind('<Leave>', lambda event: create_button.config(
            image=self.create_btn_photo))

        back_button = tk.Button(
            self.background_canvas, image=self.back_btn_photo, command=self.menu_manager.show_play_menu, borderwidth=0)
        back_button.place(x=563, y=574)
        back_button.bind('<Enter>', lambda event: back_button.config(
            image=self.hover_back_btn_photo))
        back_button.bind('<Leave>', lambda event: back_button.config(
            image=self.back_btn_photo))

    def create_room(self):
        name = self.name_entry.get()
        players = self.player_var.get()

        if name == "":
            messagebox.showerror("Error", "Masukkan nama terlebih dahulu")
        else:
            self.menu_manager.name = name
            print(f'>> Set player name to: {self.menu_manager.name}')

            room_id = "".join(str(random.randint(0, 9)) for _ in range(6))
            self.menu_manager.room_id = room_id
            print(f'>> Set room id to: {self.menu_manager.room_id}')

            send_data = {
                'command': "CREATE ROOM",
                'room_id': room_id,
                'name': name,
                'num_players': players
            }

            self.menu_manager.socket.send(pickle.dumps(send_data))
            print(f'>> Send data to server: {send_data}')

            self.menu_manager.menus["waiting_room"] = WaitingRoom(
                self.menu_manager, self.menu_manager)
            self.menu_manager.show_menu("waiting_room")

    def on_entry_click(self, event):
        if self.name_entry.get() == self.placeholder_text:
            self.name_entry.delete(0, tk.END)
            self.name_entry.configure(foreground="black")
