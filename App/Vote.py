import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pickle
import threading
import time

class Vote(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_profile()
        self.create_widgets()

        self.start_timer(8)

    def load_image(self):
        self.background_image = Image.open('assets/BgVote.png')
        self.vote_btn_image = Image.open('assets/button/Small Button Vote.png')
        self.hover_vote_btn_image = Image.open('assets/button/Small Button Vote Hover.png')
        self.disabled_vote_btn_image = Image.open('assets/button/Small Disabled Button Vote.png')

        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.vote_btn_photo = ImageTk.PhotoImage(self.vote_btn_image)
        self.hover_vote_btn_photo = ImageTk.PhotoImage(self.hover_vote_btn_image)
        self.disabled_vote_btn_photo = ImageTk.PhotoImage(self.disabled_vote_btn_image)

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

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.menu_manager.screen_width, height=self.menu_manager.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)

    def create_widgets(self):
        role = self.menu_manager.role
        name = self.menu_manager.name

        self.player = tk.StringVar(self)
        players_name = []
        data = self.menu_manager.game_info
        for player in data["player_list"]:
            if player["status"] == "alive" and player["name"] != self.menu_manager.name:
                players_name.append(player["name"])

        self.player_dropdown = ttk.OptionMenu(
            self, self.player, *players_name)
        self.player_dropdown.place(x=600, y=360)

        if self.menu_manager.status == 'dead':
            self.submit_button = tk.Label(self.background_canvas, image=self.disabled_vote_btn_photo, text="")
            self.submit_button.place(x=696, y=421)
        elif self.menu_manager.status == 'alive':
            self.vote_button = tk.Button(
                self.background_canvas, image=self.vote_btn_photo, command=self.vote, borderwidth=0)
            self.vote_button.place(x=696, y=421)
        self.vote_button.bind('<Enter>', lambda event: self.vote_button.config(
            image=self.hover_vote_btn_photo))
        self.vote_button.bind('<Leave>', lambda event: self.vote_button.config(
            image=self.vote_btn_photo))
        self.vote_button.place(x=564, y=464)

        self.timer_label = tk.Label(self.background_canvas, text='', foreground='#ECE3D5', background="#612C12",
                                    font=('Arial', 32))
        self.timer_label.place(x=950, y=590)

    def vote(self):
        pass

    def start_timer(self, seconds):
        self.remaining_time = seconds
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.configure(text=self.remaining_time)
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            pass

