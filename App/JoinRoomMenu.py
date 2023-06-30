import tkinter as tk
from tkinter import ttk
import pickle
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk

from App.WaitingRoom import WaitingRoom


class JoinRoomMenu(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_widgets()

    def load_image(self):
        self.background_image = Image.open(
            'assets/BgGabung.png')
        self.join_btn_image = Image.open(
            'assets/button/Small Button Gabung.png')
        self.hover_join_btn_image = Image.open(
            'assets/button/Small Button Gabung Hover.png')
        self.back_btn_image = Image.open(
            'assets/button/Small Button Kembali.png')
        self.hover_back_btn_image = Image.open(
            'assets/button/Small Button Kembali Hover.png')

        # Convert images to Tkinter PhotoImage objects
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.join_btn_photo = ImageTk.PhotoImage(self.join_btn_image)
        self.hover_join_btn_photo = ImageTk.PhotoImage(
            self.hover_join_btn_image)
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
        self.name_placeholder_text = "Masukkan nama anda..."
        self.name_entry.insert(0, self.name_placeholder_text)
        self.name_entry.configure(foreground="gray")
        self.name_entry.bind('<FocusIn>', self.on_name_entry_click)

        self.code_entry = ttk.Entry(
            self.background_canvas, width=40, background="#ECE3D5")
        self.code_entry.place(x=520, y=408)
        self.code_placeholder_text = "Masukkan room code..."
        self.code_entry.insert(0, self.code_placeholder_text)
        self.code_entry.configure(foreground="gray")
        self.code_entry.bind('<FocusIn>', self.on_code_entry_click)

        join_button = tk.Button(
            self.background_canvas, image=self.join_btn_photo, command=self.join_room, borderwidth=0)
        join_button.place(x=563, y=490)
        join_button.bind('<Enter>', lambda event: join_button.config(
            image=self.hover_join_btn_photo))
        join_button.bind('<Leave>', lambda event: join_button.config(
            image=self.join_btn_photo))

        back_button = tk.Button(
            self.background_canvas, image=self.back_btn_photo, command=self.menu_manager.show_play_menu, borderwidth=0)
        back_button.place(x=563, y=574)
        back_button.bind('<Enter>', lambda event: back_button.config(
            image=self.hover_back_btn_photo))
        back_button.bind('<Leave>', lambda event: back_button.config(
            image=self.back_btn_photo))

    def join_room(self):
        name = self.name_entry.get()
        room_code = self.code_entry.get()
        if name == "":
            messagebox.showerror("Error", "Masukkan nama terlebih dahulu")
        else:
            self.menu_manager.name = name
            print(f'>> Set player name to: {self.menu_manager.name}')

            self.menu_manager.room_id = room_code
            print(f'>> Set room id to: {self.menu_manager.room_id}')

            send_data = {
                'command': "CHECK ROOM",
                'room_id': room_code,
                'name': name,
            }

            self.menu_manager.socket.send(pickle.dumps(send_data))
            print(f'>> Send data to server: {send_data}')

            data = self.menu_manager.socket.recv(2048)
            data = pickle.loads(data)

            if data['status'] == 'DOES NOT EXIST':
                messagebox.showerror("Error", "Ruangan tidak ditemukan")
            else:
                send_data = {
                    'command': "JOIN ROOM",
                    'room_id': room_code,
                    'name': name,
                }

                self.menu_manager.socket.send(pickle.dumps(send_data))
                print(f'>> Send data to server: {send_data}')

                self.menu_manager.menus["waiting_room"] = WaitingRoom(
                    self.menu_manager, self.menu_manager)
                self.menu_manager.show_menu("waiting_room")

    def on_name_entry_click(self, event):
        if self.name_entry.get() == self.name_placeholder_text:
            self.name_entry.delete(0, tk.END)
            self.name_entry.configure(foreground="black")

    def on_code_entry_click(self, event):
        if self.code_entry.get() == self.code_placeholder_text:
            self.code_entry.delete(0, tk.END)
            self.code_entry.configure(foreground="black")
