import tkinter as tk
from tkinter import ttk
import pickle
import random
from PIL import Image, ImageTk
import ctypes
from App.WaitingRoom import WaitingRoom

# class yang tidak berguna :"


class CustomEntry(tk.Frame):
    def __init__(self, master, style=None, **kwargs):
        super().__init__(master, **kwargs)
        self.style = style
        self.create_widgets()

    def create_widgets(self):
        self.entry_frame = tk.Frame(self, bd=2, relief=tk.SOLID)
        self.entry_frame.pack(fill=tk.BOTH, expand=True)
        self.entry_frame.bind("<Button-1>", lambda event: self.focus_set())

        self.entry_label = ttk.Label(self.entry_frame, style=self.style)
        self.entry_label.pack(fill=tk.BOTH, expand=True)

    def get(self):
        return self.entry_label.cget("text")

    def config(self, **kwargs):
        self.entry_label.config(**kwargs)

    def insert(self, index, string):
        self.entry_label.config(text=self.entry_label.cget("text") + string)

    def delete(self, start, end=None):
        text = self.entry_label.cget("text")
        if end is None:
            self.entry_label.config(text=text[:start])
        else:
            self.entry_label.config(text=text[:start] + text[end:])


class CreateRoomMenu(tk.Frame):
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
        self.num_of_player_image = Image.open('assets/Number Of Player.png')
        self.dropdown_btn_image = Image.open('assets/drop down.png')
        self.create_room_btn_image = Image.open(
            'assets/Button Create Room.png')
        self.input_name_image = Image.open('assets/Input Name.png')
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
        self.num_of_player_image = self.num_of_player_image.resize(
            (int(self.screen_width / 8), int(self.screen_height / 24)), Image.ANTIALIAS)
        self.dropdown_btn_image = self.dropdown_btn_image.resize(
            (int(self.screen_width / 5), int(self.screen_height / 6)), Image.ANTIALIAS)
        self.create_room_btn_image = self.create_room_btn_image.resize(
            (int(self.screen_width / 10), int(self.screen_height / 16)), Image.ANTIALIAS)
        self.input_name_image = self.input_name_image.resize(
            (int(self.screen_width / 5), int(self.screen_height / 10)), Image.ANTIALIAS)
        self.back_btn_image = self.back_btn_image.resize(
            (int(self.screen_width / 10), int(self.screen_height / 16)), Image.ANTIALIAS)

        # Convert images to Tkinter PhotoImage objects
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.title_photo = ImageTk.PhotoImage(self.title_image)
        self.modal_create_room_photo = ImageTk.PhotoImage(
            self.modal_create_room_image)
        self.name_input_photo = ImageTk.PhotoImage(self.name_input_image)
        self.num_of_player_photo = ImageTk.PhotoImage(self.num_of_player_image)
        self.dropdown_btn_photo = ImageTk.PhotoImage(self.dropdown_btn_image)
        self.create_room_btn_photo = ImageTk.PhotoImage(
            self.create_room_btn_image)
        self.input_name_photo = ImageTk.PhotoImage(self.input_name_image)
        self.back_btn_photo = ImageTk.PhotoImage(
            self.back_btn_image)

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
        self.background_canvas.create_image(int(self.screen_width * 0.45), int(
            self.screen_height / 3), anchor=tk.NW, image=self.num_of_player_photo)
        # self.background_canvas.create_image(int(self.screen_width * 0.41), int(
        #     self.screen_height * 0.25), anchor=tk.NW, image=self.input_name_photo)

       # Create input field
        self.name_entry = ttk.Entry(self.background_canvas)
        self.name_entry.place(x=int(self.screen_width * 0.46),
                              y=int(self.screen_height / 4))

        self.player_var = ttk.Entry(self.background_canvas)
        self.player_var = tk.StringVar(self)
        self.player_var.set("4")
        player_dropdown = ttk.OptionMenu(
            self, self.player_var, self.player_var.get(), "4", "8", "12")
        player_dropdown.place(x=int(self.screen_width * 0.49),
                              y=int(self.screen_height / 2.5))

        create_button = ttk.Button(
            self.background_canvas, image=self.create_room_btn_photo, command=self.create_room)
        create_button.place(x=int(self.screen_width * 0.45),
                            y=int(self.screen_height * 0.6))

        create_button = ttk.Button(
            self.background_canvas, image=self.back_btn_photo, command=self.menu_manager.show_main_menu)
        create_button.place(x=int(self.screen_width * 0.45),
                            y=int(self.screen_height * 0.7))

    def create_widgets(self):
        name_label = ttk.Label(self, text="Choose Username:")
        name_label.pack()

        self.name_entry = CustomEntry(self, style="Custom.TEntry")
        self.name_entry.pack()

        player_label = ttk.Label(self, text="Number of Players:")
        player_label.pack()
        self.player_var = tk.StringVar(self)
        self.player_var.set("4")
        player_dropdown = ttk.OptionMenu(
            self, self.player_var, self.player_var.get(), "4", "8", "12")
        player_dropdown.pack()

        create_button = ttk.Button(
            self, text="Create Room", command=self.create_room)
        create_button.pack()

        back_button = ttk.Button(
            self, text="Back to Menu", command=self.menu_manager.show_main_menu)
        back_button.pack()

    def create_room(self):
        name = self.name_entry.get()
        players = self.player_var.get()
        # Code for creating a room goes here
        # You can update the window or perform any other actions

        
        self.menu_manager.name = name
        print(f'Set player name to: {self.menu_manager.name}')

        room_id_check = True
        while room_id_check:
            room_id = "".join(str(random.randint(0, 9)) for _ in range(6))
            self.menu_manager.room_id = room_id
            print(f'Set room id to: {self.menu_manager.room_id}')

            send_data = {
                'command' : "CHECK ROOM ID",
                'room_id' : room_id,
                'name': name
            }

            self.menu_manager.socket.send(pickle.dumps(send_data))
            print(f'Send data to server: {send_data}')

            data = self.menu_manager.socket.recv(2048)
            data = pickle.loads(data)

            if data['status'] == 'ROOM ID DOES NOT EXIST':
                room_id_check = False

        send_data = {
            'command': "CREATE ROOM",
            'room_id': room_id,
            'name': name,
            'players': players
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))
        print(f'Send data to server: {send_data}')

        self.menu_manager.menus["waiting_room"] = WaitingRoom(
            self.menu_manager, self.menu_manager)
        self.menu_manager.show_menu("waiting_room")
