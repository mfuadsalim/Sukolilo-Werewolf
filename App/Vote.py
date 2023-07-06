import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pickle
import threading
import time

from App.VoteResult import VoteResult

class Vote(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_widgets()

        self.start_timer(8)

    def load_image(self):
        self.background_image = Image.open('assets/BgVote.png')
        self.vote_btn_image = Image.open('assets/button/Small Button Vote.png')
        self.hover_vote_btn_image = Image.open('assets/button/Small Button Vote Hover.png')

        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.vote_btn_photo = ImageTk.PhotoImage(self.vote_btn_image)
        self.hover_vote_btn_photo = ImageTk.PhotoImage(self.hover_vote_btn_image)

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

        self.vote_button = tk.Button(
            self.background_canvas, image=self.vote_btn_photo, command=self.vote, borderwidth=0)
        self.vote_button.place(x=696, y=421)
        self.vote_button.bind('<Enter>', lambda event: self.vote_button.config(
            image=self.hover_vote_btn_photo))
        self.vote_button.bind('<Leave>', lambda event: self.vote_button.config(
            image=self.vote_btn_photo))
        self.vote_button.place(x=564, y=464)

        text = f"{name}({role})"
        self.name_role_text = tk.Label(self.background_canvas, text=text, foreground="#37342f", background='#ECE3D5',
                                       font=('Arial', 12))
        self.name_role_text.place(x=291, y=620)

        self.timer_label = tk.Label(self.background_canvas, text='', foreground='#ECE3D5', background="#612C12",
                                    font=('Arial', 32))
        self.timer_label.place(x=945, y=585)

    def vote(self):
        player_voted = self.player.get()

        send_data = {
            'command': "VOTE",
            'room_id': self.menu_manager.room_id,
            'role': self.menu_manager.role,
            'name': self.menu_manager.name,
            'player_voted': player_voted,
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))
        print(f">> Send data to server: {send_data}")

        self.player_dropdown.destroy()
        self.vote_button.destroy()

        text = f"Anda telah melakukan vote kepada: {player_voted}"
        text_after_vote = tk.Label(self.background_canvas, text=text, background='#ECE3D5',
                                  font=('Arial', 12))
        text_after_vote.place(x=470, y=360)

    def start_timer(self, seconds):
        self.remaining_time = seconds
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.configure(text=self.remaining_time)
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            self.menu_manager.menus["vote_result"] = VoteResult(
                self.menu_manager, self.menu_manager)
            self.menu_manager.show_menu("vote_result")

