import tkinter as tk
from PIL import Image, ImageTk
import pickle
import threading
import time

from App.Chat import Chat

class Day(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_profile()
        self.create_widgets()
        self.show_summary()
        self.start_timer(8)

    def load_image(self):
        self.background_image = Image.open('assets/BgSiang.png')

        self.background_photo = ImageTk.PhotoImage(self.background_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.menu_manager.screen_width, height=self.menu_manager.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)
    
    def create_profile(self):
        self.avatar_mahasiswa_image = Image.open('assets/AvatarMahasiswaDay.png')
        self.avatar_mahasiswa_photo = ImageTk.PhotoImage(self.avatar_mahasiswa_image)

        self.avatar_dead_image = Image.open('assets/AvatarDead.png')
        self.avatar_dead_photo = ImageTk.PhotoImage(self.avatar_dead_image)

        self.avatar_werewolf_dead_image = Image.open('assets/AvatarWerewolfDead.png')
        self.avatar_werewolf_dead_photo = ImageTk.PhotoImage(self.avatar_werewolf_dead_image)

        player_avatars = []
        player_names = []

        data = self.menu_manager.game_info

        for count, player in enumerate(data["player_list"]):
            player_name = tk.Label(self.background_canvas, text=player['name'], background='#1DAAD6', foreground='#ECE3D5',
                                    font=('Arial', 12))
            if player['status'] == 'dying':
                if player['role'] == 'Werewolf':
                    avatar = tk.Label(self.background_canvas, image=self.avatar_werewolf_dead_photo, background='#1DAAD6')
                else:
                    avatar = tk.Label(self.background_canvas, image=self.avatar_dead_photo, background='#1DAAD6')
            else:
                avatar = tk.Label(self.background_canvas, image=self.avatar_mahasiswa_photo, background='#1DAAD6')

            if self.menu_manager.num_players == '4':
                if count < 2:
                    avatar.place(x=126, y=260+160*count)
                    player_name.place(x=126, y=340+160*count)
                else:
                    avatar.place(x=1090, y=260+160*(count%2))
                    player_name.place(x=1090, y=340+160*(count%2))
            
            elif self.menu_manager.num_players == '8':
                if count < 4:
                    avatar.place(x=126, y=175+120*count)
                    player_name.place(x=126, y=255+120*count)
                else:
                    avatar.place(x=1090, y=175+120*(count%4))
                    player_name.place(x=1090, y=255+120*(count%4))
            
            elif self.menu_manager.num_players == '12':
                if count < 2:
                    avatar.place(x=49, y=175+120*(1+count))
                    player_name.place(x=49, y=255+120*(1+count))
                elif count < 6:
                    avatar.place(x=154, y=175+120*(count-2))
                    player_name.place(x=154, y=255+120*(count-2))
                elif count < 10:
                    avatar.place(x=1066, y=175+120*(count-6))
                    player_name.place(x=1066, y=255+120*(count-6))
                else:
                    avatar.place(x=1172, y=175+120*(1+count-10))
                    player_name.place(x=1172, y=255+120*(1+count-10))

            player_avatars.append(avatar)
            player_names.append(player_name)

    def create_widgets(self):
        self.timer_label = tk.Label(self.background_canvas, text='', foreground='#ECE3D5', background="#612C12",
                                    font=('Arial', 32))
        self.timer_label.place(x=945, y=550)

    def show_summary(self):
        any_death = False
        data = self.menu_manager.game_info
        player_list = data["player_list"]

        text = ""

        for player in player_list:
            if player["status"] == 'dying':
                if any_death == False: any_death = True
                if player["role"] == "Werewolf":
                    text = text + f"Pemburu berhasil membunuh Werewolf yang ternyata adalah {player['name']}.\n"
                else:
                    text = text + f"Telah ditemukan bahwa {player['name']} mati terbunuh.\n"
            elif player["status"] == 'dispelled':
                if any_death == False: any_death = True
                text = text + f"Terdapat bekas tusukan parah pada {player['name']}, tetapi {player['name']} selamat\n"

        if any_death == False:
            text = "Tadi malam, Sukolilo terjaga dengan aman, tidak ada korban jiwa."

        self.text = tk.Label(self.background_canvas, text=text, foreground="#37342f", background='#ECE3D5', font=('Arial', 12))
        self.text.place(x=400, y=350)
        self.is_running = False

    def start_timer(self, seconds):
        self.remaining_time = seconds
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.configure(text=self.remaining_time)
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            send_data = {
                'command': "SUMMARIZE NIGHT",
                'name': self.menu_manager.name,
                'room_id': self.menu_manager.room_id,
            }

            self.menu_manager.socket.send(pickle.dumps(send_data))

            print(f">> Send data to server: {send_data}")

            is_receiving = True

            while is_receiving:
                data = self.menu_manager.socket.recv(2048)
                data = pickle.loads(data)

                if data['command'] == "SUMMARIZED NIGHT": 
                    is_receiving = False

            self.menu_manager.game_info = data["game_info"]

            print(data["game_info"])

            self.is_running = False
            self.menu_manager.menus["chat"] = Chat(
                self.menu_manager, self.menu_manager)
            self.menu_manager.show_menu("chat")
