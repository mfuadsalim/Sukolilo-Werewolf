import tkinter as tk
from tkinter import ttk


class WelcomeGame(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.create_widgets()

    def create_widgets(self):
        num_player_label = ttk.Label(self, text="Role:")
        num_player_label.pack()

        data = self.menu_manager.game_info

        for player in data["player_list"]:
            if player["name"] == self.menu_manager.name:
                role_text = player["role"]

        self.num_player_value = ttk.Label(self, text=role_text)
        self.num_player_value.pack()
