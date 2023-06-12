import tkinter as tk
from tkinter import ttk
import pickle

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
        # Perform start game logic here
        pass