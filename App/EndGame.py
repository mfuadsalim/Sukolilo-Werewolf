import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pickle
import threading
import time

class EndGame(tk.Frame):
    def __init__(self, master, menu_manager, winner):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.winner = winner
        self.load_image()
        self.create_canvas()
        self.create_profile()
        self.create_widgets()

    def load_image(self):
        self.background_image = Image.open('assets/BgGameSelesai.png')
        self.warga_menang_image = Image.open('assets/TimWargaMenang.png')
        self.warga_kalah_image = Image.open('assets/TimWargaKalah.png')
        self.werewolf_menang_image = Image.open('assets/TimWerewolfMenang.png')
        self.werewolf_kalah_image = Image.open('assets/TimWerewolfKalah.png')


        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.warga_menang_photo = ImageTk.PhotoImage(self.warga_menang_image)
        self.warga_kalah_photo = ImageTk.PhotoImage(self.warga_kalah_image)
        self.werewolf_menang_photo = ImageTk.PhotoImage(self.werewolf_menang_image)
        self.werewolf_kalah_photo = ImageTk.PhotoImage(self.werewolf_kalah_image)

        self.back_btn_image = Image.open(
            'assets/button/Small Button Kembali.png')
        self.hover_back_btn_image = Image.open(
            'assets/button/Small Button Kembali Hover.png')

        self.back_btn_photo = ImageTk.PhotoImage(self.back_btn_image)
        self.hover_back_btn_photo = ImageTk.PhotoImage(
            self.hover_back_btn_image)

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
        if (self.winner == 'warga'):
            text = f"Karena sudah tidak ada lagi warga yang\ntersisa di Sukolilo, game sudah berakhir"
            if (self.menu_manager.team == 'Warga'):
                self.sign = tk.Label(self.background_canvas, image=self.warga_kalah_photo, background='#ECE3D5')
            else:
                self.sign = tk.Label(self.background_canvas, image=self.werewolf_menang_photo, background='#ECE3D5')
        else:
            text = f"Karena sudah tidak ada lagi Werewolf yang\ntersisa di Sukolilo, game sudah berakhir"
            if (self.menu_manager.team == 'Warga'):
                self.sign = tk.Label(self.background_canvas, image=self.warga_menang_photo, background='#ECE3D5')
            else:
                self.sign = tk.Label(self.background_canvas, image=self.werewolf_kalah_photo, background='#ECE3D5')

        self.conclusion_text = tk.Label(self.background_canvas, text=text, background='#ECE3D5',
                                   font=('Arial', 12))
        self.conclusion_text.place(x=480, y=220)
        self.sign.place(x=473, y=292)

        back_button = tk.Button(
            self.background_canvas, image=self.back_btn_photo, command=self.menu_manager.show_play_menu, borderwidth=0)
        back_button.place(x=565, y=565)
        back_button.bind('<Enter>', lambda event: back_button.config(
            image=self.hover_back_btn_photo))
        back_button.bind('<Leave>', lambda event: back_button.config(
            image=self.back_btn_photo))

