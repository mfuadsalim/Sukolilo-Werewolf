import tkinter as tk
from tkinter import ttk
import pickle
import random

class WaitingRoom(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager

        self.room_code = tk.StringVar()
        self.player_list = tk.StringVar()
        
        self.create_widgets()

    def create_widgets(self):
        send_data = {
            'command' : "GET DETAIL ROOM",
            'room_id' : self.menu_manager.room_id,
            'name'    : self.menu_manager.name
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))
        print(f'Send data to server: {send_data}')

        data = self.menu_manager.socket.recv(2048)
        data = pickle.loads(data)

        print(data)

        room_code_label = ttk.Label(self, text='Room Code: ')
        room_code_label.pack()

        room_code_value = ttk.Label(self, text=self.menu_manager.room_id)
        room_code_value.pack()
        
        num_player_label = ttk.Label(self, text="Num Player:")
        num_player_label.pack()

        num_player_value = ttk.Label(self, text=data['num_players'])
        num_player_value.pack()

        player_list_label = ttk.Label(self, text="Player List:")
        player_list_label.pack()

        player_string = '\n'.join(data['player_list'])
        player_list_value = ttk.Label(self, text=player_string)
        player_list_value.pack()

        start_button = ttk.Button(self, text="Start", command=self.start_game)
        start_button.pack()

    def start_game(self):
        data = self.menu_manager.socket.recv(2048)
        data = pickle.loads(data)

        num_players = int(data['num_players'])
        if num_players == 4:
            avatars = ['Werewolf', 'Seeker/Sheer', 'Villager', 'Villager']
        elif num_players == 8:
            avatars = ['Werewolf', 'Werewolf', 'Seeker', 'Seeker', 'Villager', 'Villager', 'Villager', 'Villager']
        elif num_players == 12:
            avatars = ['Werewolf', 'Werewolf', 'Werewolf', 'Seeker/Sheer', 'Seeker/Sheer', 'Seeker/Sheer', 'Villager', 'Villager', 'Villager', 'Villager', 'Villager', 'Villager']
        else:
            print("Invalid number of players.")
            return

        random.shuffle(avatars)

        # Perform start game logic with avatars here
        for i, player in enumerate(data['player_list']):
            avatar = avatars[i]
            print(f"Player: {player}, Avatar: {avatar}")

        # Example: You can update the player list labels with avatars instead of names
        player_string = '\n'.join(avatars)
        self.player_list_value.configure(text=player_string)