import tkinter as tk
from tkinter import ttk
import pickle
import random

from App.WaitingRoom import WaitingRoom

class CreateRoomMenu(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.create_widgets()

    def create_widgets(self):
        name_label = ttk.Label(self, text="Name:")
        name_label.pack()
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack()

        player_label = ttk.Label(self, text="Number of Players:")
        player_label.pack()
        self.player_var = tk.StringVar(self)
        self.player_var.set("4")
        player_dropdown = ttk.OptionMenu(self, self.player_var, self.player_var.get(), "4", "8", "12")
        player_dropdown.pack()

        create_button = ttk.Button(self, text="Create Room", command=self.create_room)
        create_button.pack()

        back_button = ttk.Button(self, text="Back to Menu", command=self.menu_manager.show_main_menu)
        back_button.pack()

    def create_room(self):
        name = self.name_entry.get()
        players = self.player_var.get()
        # Code for creating a room goes here
        # You can update the window or perform any other actions
        
        self.menu_manager.name = name
        print(f'Set player name to: {self.menu_manager.name}')

        room_id = "".join(str(random.randint(0, 9)) for _ in range(6))
        self.menu_manager.room_id = room_id
        print(f'Set room id to: {self.menu_manager.room_id}')


        send_data = {
            'command' : "CREATE ROOM",
            'room_id' : room_id,
            'name': name,
            'players': players
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))
        print(f'Send data to server: {send_data}')

        self.menu_manager.menus["waiting_room"] = WaitingRoom(self.menu_manager, self.menu_manager)
        self.menu_manager.show_menu("waiting_room")