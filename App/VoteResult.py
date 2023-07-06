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
        self.create_widgets()

        self.start_timer(8)

    def load_image(self):
        self.background_image = Image.open('assets/BgVoteResult.png')

        self.background_photo = ImageTk.PhotoImage(self.background_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.menu_manager.screen_width, height=self.menu_manager.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)

    def create_widgets(self):
        role = self.menu_manager.role
        name = self.menu_manager.name

        send_data = {
            'command': "VOTE RESULT",
            'room_id': self.menu_manager.room_id,
            'role': self.menu_manager.role,
            'name': self.menu_manager.name,
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))
        self.menu_manager.socket.send(pickle.dumps(send_data))
        print(f">> Send data to server: {send_data}")

        data = self.menu_manager.socket.recv(2048)
        data = pickle.loads(data)

        if data["command"] == "RESPONSE VOTE RESULT":
            self.menu_manager.game_info = data["game_info"]
            text=data["vote_result"]

        self.text_after_vote = tk.Label(self.background_canvas, text=text, background='#ECE3D5',
                                   font=('Arial', 12))
        self.text_after_vote.place(x=470, y=360)

        text = f"{name}({role})"
        self.name_role_text = tk.Label(self.background_canvas, text=text, foreground="#37342f", background='#ECE3D5',
                                       font=('Arial', 12))
        self.name_role_text.place(x=291, y=620)

        self.timer_label = tk.Label(self.background_canvas, text='', foreground='#ECE3D5', background="#612C12",
                                    font=('Arial', 32))
        self.timer_label.place(x=945, y=585)

    def start_timer(self, seconds):
        self.remaining_time = seconds
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.configure(text=self.remaining_time)
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            self.menu_manager.show_menu("night")
