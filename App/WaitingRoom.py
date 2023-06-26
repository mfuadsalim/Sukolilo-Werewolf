import tkinter as tk
from tkinter import ttk
import pickle
import random
import threading
import tkinter.messagebox as messagebox

from App.WelcomeGame import WelcomeGame


class WaitingRoom(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager

        self.room_code = tk.StringVar()
        self.player_list = tk.StringVar()

        self.create_widgets()

        # Start a separate thread to continuously update the player list
        self.update_thread = threading.Thread(target=self.update)
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

        self.start_button = ttk.Button(
            self, text="Start", command=self.start_game)
        self.start_button.pack()

    def update(self):
        while True:
            send_data = {
                'command': "GET DETAIL ROOM",
                'room_id': self.menu_manager.room_id,
                'name': self.menu_manager.name
            }

            self.menu_manager.socket.send(pickle.dumps(send_data))

            try:
                data = self.menu_manager.socket.recv(2048)
                data = pickle.loads(data)
                if data["command"] == "GET DETAIL ROOM":
                    # Access the 'num_players' value
                    num_players = data["game_info"]['num_players']
                    # Access the 'player_list' value
                    player_list = data["game_info"]['player_list']
                    player_names = '\n'.join([player['name']
                                              for player in player_list])

                    self.num_player_value.config(text=num_players)
                    self.player_list_value.config(text=player_names)

                    if int(num_players) != len(player_list):
                        self.start_button.state(['disabled'])
                    else:
                        self.start_button.state(['!disabled'])

                    self.menu_manager.game_info = data["game_info"]

                if data["command"] == "START GAME":
                    self.menu_manager.game_info = data["game_info"]
                    print(self.menu_manager.game_info)

                    self.menu_manager.menus["welcome_game"] = WelcomeGame(
                        self.menu_manager, self.menu_manager)
                    self.menu_manager.show_menu("welcome_game")
            except:
                pass

    def start_game(self):
        send_data = {
            'command': "GENERATE AVATAR",
            'room_id': self.menu_manager.room_id,
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))
