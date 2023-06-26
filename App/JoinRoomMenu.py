import tkinter as tk
from tkinter import ttk
import pickle
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import ctypes

from App.WaitingRoom import WaitingRoom


class JoinRoomMenu(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        # self.create_widgets()

    def load_image(self):
        self.background_image = Image.open(
            'assets/Create Room - Backround.png')
        self.title_image = Image.open('assets/Sukolilo WereWolf.png')
        self.modal_create_room_image = Image.open(
            'assets/Modal Create Room.png')
        self.name_input_image = Image.open('assets/Name.png')
        self.room_code_image = Image.open('assets/Room Code.png')
        self.join_room_btn_image = Image.open(
            'assets/Button Join Room.png')
        self.back_btn_image = Image.open('assets/Button Back.png')

        # Get screen resolution
        user32 = ctypes.windll.user32
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)

        # Resize images based on screen resolution
        self.background_image = self.background_image.resize(
            (self.screen_width, self.screen_height), Image.ANTIALIAS)
        self.title_image = self.title_image.resize(
            (int(self.screen_width / 6), int(self.screen_height / 9)), Image.ANTIALIAS)
        self.modal_create_room_image = self.modal_create_room_image.resize(
            (int(self.screen_width*0.4), int(self.screen_height*0.8)), Image.ANTIALIAS)
        self.name_input_image = self.name_input_image.resize(
            (int(self.screen_width / 15), int(self.screen_height / 24)), Image.ANTIALIAS)
        self.room_code_image = self.room_code_image.resize(
            (int(self.screen_width / 15), int(self.screen_height / 24)), Image.ANTIALIAS)
        self.join_room_btn_image = self.join_room_btn_image.resize(
            (int(self.screen_width / 10), int(self.screen_height / 16)), Image.ANTIALIAS)
        self.back_btn_image = self.back_btn_image.resize(
            (int(self.screen_width / 10), int(self.screen_height / 16)), Image.ANTIALIAS)

        # Convert images to Tkinter PhotoImage objects
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.title_photo = ImageTk.PhotoImage(self.title_image)
        self.modal_create_room_photo = ImageTk.PhotoImage(
            self.modal_create_room_image)
        self.name_input_photo = ImageTk.PhotoImage(self.name_input_image)
        self.room_code_photo = ImageTk.PhotoImage(self.room_code_image)
        self.join_room_btn_photo = ImageTk.PhotoImage(self.join_room_btn_image)
        self.back_btn_photo = ImageTk.PhotoImage(self.back_btn_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.screen_width, height=self.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)
        self.background_canvas.create_image(int(self.screen_width / 100), int(
            self.screen_height / 100), anchor=tk.NW, image=self.title_photo)
        self.background_canvas.create_image(int(self.screen_width * 0.3), int(
            self.screen_height / 12), anchor=tk.NW, image=self.modal_create_room_photo)
        self.background_canvas.create_image(int(self.screen_width * 0.475), int(
            self.screen_height / 5), anchor=tk.NW, image=self.name_input_photo)
        self.background_canvas.create_image(int(self.screen_width * 0.475), int(
            self.screen_height / 3), anchor=tk.NW, image=self.room_code_photo)
        # self.background_canvas.create_image(int(self.screen_width * 0.41), int(
        #     self.screen_height * 0.25), anchor=tk.NW, image=self.input_name_photo)

       # Create input field
        self.name_entry = ttk.Entry(self.background_canvas)
        self.name_entry.place(x=int(self.screen_width * 0.46),
                              y=int(self.screen_height / 4))

        create_button = ttk.Button(
            self.background_canvas, image=self.join_room_btn_photo, command=self.join_room)
        create_button.place(x=int(self.screen_width * 0.45),
                            y=int(self.screen_height * 0.6))

        self.code_entry = ttk.Entry(self.background_canvas)
        self.code_entry.place(x=int(self.screen_width * 0.46),
                              y=int(self.screen_height * 0.4))

        create_button = ttk.Button(
            self.background_canvas, image=self.back_btn_photo, command=self.menu_manager.show_main_menu)
        create_button.place(x=int(self.screen_width * 0.45),
                            y=int(self.screen_height * 0.7))

    def create_widgets(self):
        name_label = ttk.Label(self, text="Name:")
        name_label.pack()
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack()

        code_label = ttk.Label(self, text="Room Code:")
        code_label.pack()
        self.code_entry = ttk.Entry(self)
        self.code_entry.pack()

        join_button = ttk.Button(
            self, text="Join Room", command=self.join_room)
        join_button.pack()

        back_button = ttk.Button(
            self, text="Back to Menu", command=self.menu_manager.show_main_menu)
        back_button.pack()

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
