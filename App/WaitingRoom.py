import tkinter as tk
from tkinter import ttk
import pickle
import random
import threading


class WaitingRoom(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager

        self.room_code = tk.StringVar()
        self.player_list = tk.StringVar()

        self.create_widgets()

        # Start a separate thread to continuously update the player list
        self.update_thread = threading.Thread(target=self.get_player_list)
        # Set the thread as a daemon to stop it when the main thread exits
        self.update_thread.daemon = True
        self.update_thread.start()

    def create_widgets(self):
        room_code_label = ttk.Label(self, text='Room Code: ')
        room_code_label.pack()

        room_code_value = ttk.Label(self, text=self.menu_manager.room_id)
        room_code_value.pack()

        num_player_label = ttk.Label(self, text="Num Player:")
        num_player_label.pack()

        self.num_player_value = ttk.Label(self, text="")
        self.num_player_value.pack()

        player_list_label = ttk.Label(self, text="Player List:")
        player_list_label.pack()

        self.player_list_value = ttk.Label(self, text="")
        self.player_list_value.pack()

        start_button = ttk.Button(self, text="Start", command=self.start_game)
        start_button.pack()

    def get_player_list(self):
        while True:
            send_data = {
                'command': "GET DETAIL ROOM",
                'room_id': self.menu_manager.room_id,
                'name': self.menu_manager.name
            }

            self.menu_manager.socket.send(pickle.dumps(send_data))

            data = self.menu_manager.socket.recv(2048)
            data = pickle.loads(data)

            num_players = data['num_players']  # Access the 'num_players' value
            player_list = data['player_list']  # Access the 'player_list' value
            player_names = '\n'.join([player['name']
                                     for player in player_list])

            self.num_player_value.config(text=num_players)
            self.player_list_value.config(text=player_names)

            self.menu_manager.game_info = data

    def start_game(self):
        pass
