import tkinter as tk
import pickle
from PIL import Image, ImageTk
import threading
import time

from App.PlayerIntroduction import PlayerIntroduction

class WaitingRoom(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager

        self.load_image()
        self.create_canvas()
        self.room_code = tk.StringVar()
        self.player_list = tk.StringVar()

        self.create_widgets()

        # Start a separate thread to continuously update the player list
        self.waiting_room_thread = threading.Thread(target=self.update)
        self.is_running = True
        # Set the thread as a daemon to stop it when the main thread exits
        self.waiting_room_thread.daemon = True
        self.waiting_room_thread.start()

    def load_image(self):
        self.background_image = Image.open('assets/BgWaitingRoom.png')
        self.start_btn_image = Image.open('assets/button/Small Button Siap.png')
        self.hover_start_btn_image = Image.open('assets/button/Small Button Siap Hover.png')
        self.disabled_start_btn_image = Image.open('assets/button/Small Disabled Button Siap.png')

        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.start_btn_photo = ImageTk.PhotoImage(self.start_btn_image)
        self.hover_start_btn_photo = ImageTk.PhotoImage(self.hover_start_btn_image)
        self.disabled_start_btn_photo = ImageTk.PhotoImage(self.disabled_start_btn_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.menu_manager.screen_width, height=self.menu_manager.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)

    def create_widgets(self):
        room_code_value = tk.Label(self.background_canvas, text=self.menu_manager.room_id, background='#ECE3D5', font=('Arial', 12))
        room_code_value.place(x=497, y=190)

        self.num_player_value = tk.Label(self.background_canvas, text="", background='#ECE3D5', font=('Arial', 12))
        self.num_player_value.place(x=846, y=190)

        self.player_list_value = tk.Label(self.background_canvas, text="", background='#ECE3D5', font=('Arial', 12))
        self.player_list_value.place(x=550, y=275)

        self.ready_player_num = tk.Label(self.background_canvas, text="", background='#ECE3D5', font=('Arial', 12))
        self.ready_player_num.place(x=710, y=505)

    def update(self):
        while self.is_running:
            send_data = {
                'command': "GET DETAIL ROOM",
                'room_id': self.menu_manager.room_id,
                'name': self.menu_manager.name
            }

            self.menu_manager.socket.send(pickle.dumps(send_data))
            # print(f'>> Send data to server: {send_data}')

            try:
                data = self.menu_manager.socket.recv(2048)
                data = pickle.loads(data)
                # print(data)
                if data["command"] == "GET DETAIL ROOM":
                    # Access the 'num_players' value
                    num_players = data["game_info"]['num_players']
                    # Access the 'player_list' value
                    player_list = data["game_info"]['player_list']
                    player_names = '\n'.join([player['name']
                                              for player in player_list])
                    # Count the 'ready_player_num' value and search for player object
                    menu_player = {}
                    player_ready = 0
                    total_player = 0
                    for player in player_list:
                        if (player['name'] == self.menu_manager.name):
                            menu_player = player

                        if (player['is_ready']): 
                            player_ready += 1
                        total_player += 1

                    self.num_player_value.config(text=num_players)
                    self.player_list_value.config(text=player_names)
                    self.ready_player_num.config(text=f"{player_ready}/{total_player}")

                    if int(num_players) != len(player_list) or menu_player['is_ready']:
                        disabled_start_button = tk.Label(self.background_canvas, image=self.disabled_start_btn_photo, text="")
                        disabled_start_button.place(x=564, y=559)
                    else:
                        start_button = tk.Button(
                            self.background_canvas, image=self.start_btn_photo, borderwidth=0,
                            command=self.ready)
                        start_button.place(x=564, y=559)
                        start_button.bind('<Enter>', lambda event: start_button.config(
                            image=self.hover_start_btn_photo))
                        start_button.bind('<Leave>', lambda event: start_button.config(
                            image=self.start_btn_photo))
                        
                    if player_ready == total_player:
                        self.start_game()

                    self.menu_manager.game_info = data["game_info"]

                if data["command"] == "START GAME":
                    self.menu_manager.game_info = data["game_info"]

                    data = self.menu_manager.game_info
                    for player in data["player_list"]:
                        if player["name"] == self.menu_manager.name:
                            self.menu_manager.role = player["role"]

                    self.menu_manager.num_players = num_players

                    print(f">> Set role to: {self.menu_manager.role}")

                    if self.menu_manager.role == "Werewolf":
                        self.menu_manager.action = "Bunuh"
                    elif self.menu_manager.role == "Peneliti":
                        self.menu_manager.action = "Memeriksa Identitas Pemain"
                    elif self.menu_manager.role == "Hunter":
                        self.menu_manager.action = "Bunuh"
                    elif self.menu_manager.role == "Dokter":
                        self.menu_manager.action = "Melindungi"
                    else:
                        self.menu_manager.action = None
                    
                    if self.menu_manager.role == "Werewolf":
                        self.menu_manager.team = "Werewolf"
                    else:
                        self.menu_manager.team = "Warga"

                    self.is_running = False

                    self.menu_manager.menus["player_introduction"] = PlayerIntroduction(
                        self.menu_manager, self.menu_manager)
                    self.menu_manager.show_menu("player_introduction")
            except:
                pass

            time.sleep(2)
    
    def ready(self):
        disabled_start_button = tk.Label(self.background_canvas, image=self.disabled_start_btn_photo, text="")
        disabled_start_button.place(x=564, y=559)
        
        send_data = {
            'command': "PLAYER READY",
            'room_id': self.menu_manager.room_id,
            'name': self.menu_manager.name
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))

    def start_game(self):
        send_data = {
            'command': "GENERATE AVATAR",
            'room_id': self.menu_manager.room_id,
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))
        print(f'>> Send data to server: {send_data}')

