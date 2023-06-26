import tkinter as tk
from tkinter import ttk

class HowToPlayMenu(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.create_widgets()

    def create_widgets(self):
        # Code for displaying the instructions for playing the game goes here
        # You can update the window or perform any other actions
        num_player_label = ttk.Label(self, text="Players List:")
        num_player_label.pack()

        back_button = ttk.Button(self, text="Back to Menu", command=self.menu_manager.show_main_menu)
        back_button.pack()