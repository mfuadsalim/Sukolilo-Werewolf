import tkinter as tk
from tkinter import ttk
import socket

# Import Class
from App.MainMenu import MainMenu
from App.MainInit import MainInit
from App.CreateRoomMenu import CreateRoomMenu
from App.JoinRoomMenu import JoinRoomMenu
from App.HowToPlayMenu import HowToPlayMenu


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SUKOLILO WEREWOLF")
        self.state('zoomed')  # Maximize the window
        self.server_host = 'localhost'
        self.server_port = 5000
        self.menus = {}
        self.socket = None
        self.name = None
        self.room_id = None
        self.game_info = None
        self.connect_to_server()
        self.create_menu_instances()
        self.current_menu = None
        self.show_main_menu()
        self.configure_style()

    def connect_to_server(self):
        try:
            # Update with the server address and port
            server_address = (self.server_host, self.server_port)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(server_address)
            # Perform any other actions with the connected socket if needed
            print(
                f"Welcome to Sukolilo Werewolf. Server running on {self.server_host} port {self.server_port}\n")
        except ConnectionError:
            # Handle connection error
            pass

    def create_menu_instances(self):
        self.menus["main"] = MainInit(self, self)
        self.menus["play"] = MainMenu(self, self)
        self.menus["create"] = CreateRoomMenu(self, self)
        self.menus["join"] = JoinRoomMenu(self, self)
        self.menus["how_to_play"] = HowToPlayMenu(self, self)

    def configure_style(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 12))

    def show_main_menu(self):
        self.show_menu("main")

    def show_menu(self, menu_name):
        if self.current_menu:
            self.current_menu.pack_forget()
        self.current_menu = self.menus[menu_name]
        self.current_menu.pack(expand=True)


if __name__ == "__main__":
    menu_manager = Main()
    menu_manager.mainloop()
