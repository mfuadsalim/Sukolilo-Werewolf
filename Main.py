import tkinter as tk
from tkinter import ttk
import socket

# Import Class
from App.MainMenu import MainMenu
from App.PlayMenu import PlayMenu
from App.CreateRoomMenu import CreateRoomMenu
from App.JoinRoomMenu import JoinRoomMenu
from App.AboutMenu import AboutMenu


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        # Window Configuration
        self.title("SUKOLILO WEREWOLF")
        self.screen_width = 1280
        self.screen_height = 720
        self.geometry(f"{self.screen_width}x{self.screen_height}")
        self.resizable(False, False)
        # # Get screen resolution
        # user32 = ctypes.windll.user32
        # self.screen_width = user32.GetSystemMetrics(0)
        # self.screen_height = user32.GetSystemMetrics(1)
        # Game Attributes
        self.server_host = 'localhost'
        self.server_port = 5000
        self.menus = {}
        self.socket = None
        self.name = None
        self.role = None
        self.room_id = None
        self.game_info = None
        self.current_menu = None
        self.connect_to_server()
        self.create_menu_instances()
        self.show_main_menu()
        self.configure_style()

    def connect_to_server(self):
        try:
            server_address = (self.server_host, self.server_port)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(server_address)
            print(
                "============================================================================")
            print(
                f"Welcome to Sukolilo Werewolf. Server running on {self.server_host} port {self.server_port}")
            print(
                "============================================================================\n")
        except ConnectionError:
            pass

    def create_menu_instances(self):
        self.menus["main"] = MainMenu(self, self)
        self.menus["about"] = AboutMenu(self, self)
        self.menus["play"] = PlayMenu(self, self)
        self.menus["create"] = CreateRoomMenu(self, self)
        self.menus["join"] = JoinRoomMenu(self, self)

    def configure_style(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 12))

    def show_play_menu(self):
        self.show_menu("play")

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
