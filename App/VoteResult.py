import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pickle
import threading
import time

class VoteResult(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.get_vote_result()
        self.create_profile()
        self.create_widgets()

        self.start_timer(3)

    def get_vote_result(self):
        send_data = {
            'command': "VOTE RESULT",
            'room_id': self.menu_manager.room_id,
            'name': self.menu_manager.name,
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))
        self.menu_manager.socket.send(pickle.dumps(send_data))
        print(f">> Send data to server: {send_data}")

        data = self.menu_manager.socket.recv(2048)
        data = pickle.loads(data)
        
        self.menu_manager.game_info = data["game_info"]
        self.vote_result = data['vote_result']
        self.voted_role = data['voted_role']

    def load_image(self):
        self.background_image = Image.open('assets/BgVoteResult.png')
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
            if player['status'] == 'dead':
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
        if (self.vote_result):
            text = f"Berdasarkan voting terbanyak, {self.vote_result} akan menjalani hukuman mati\nIdentitas asli {self.vote_result} adalah {self.voted_role}"
        else:
            text = f"Berdasarkan hasil voting, terdapat skor seri sehingga\ntidak ada yang menjalani hukuman mati"

        self.text_after_vote = tk.Label(self.background_canvas, text=text, background='#ECE3D5',
                                   font=('Arial', 12))
        self.text_after_vote.place(x=400, y=360)

        self.timer_label = tk.Label(self.background_canvas, text='', foreground='#ECE3D5', background="#612C12",
                                    font=('Arial', 32))
        self.timer_label.place(x=950, y=590)

    def start_timer(self, seconds):
        self.remaining_time = seconds
        self.update_timer()

    def update_timer(self):
        from App.Night import Night
        from App.EndGame import EndGame

        if self.remaining_time > 0:
            self.timer_label.configure(text=self.remaining_time)
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            data = self.menu_manager.game_info

            warga = 0
            werewolf = 0

            for player in data["player_list"]:
                # set menu_manager status
                if player['name'] == self.menu_manager.name:
                    if player['status'] == 'dead':
                        self.menu_manager.status = 'dead'
                    elif player['status'] == 'alive':
                        self.menu_manager.status = 'alive'
                
                # check for end game condition
                if player['status'] == 'alive':
                    if player['role'] == 'Werewolf':
                        werewolf += 1
                    else: warga += 1

            print(warga)
            print(werewolf)
            
            if warga == 0 or werewolf == 0:
                if warga == 0: winner = 'warga'
                else: winner = 'werewolf'

                self.menu_manager.menus["end_game"] = EndGame(
                    self.menu_manager, self.menu_manager, winner)
                self.menu_manager.show_menu("end_game")
            
            else:
                self.menu_manager.menus["night"] = Night(
                    self.menu_manager, self.menu_manager)
                self.menu_manager.show_menu("night")

