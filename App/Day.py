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
        self.create_widgets()

        self.day_thread = threading.Thread(target=self.update)
        self.is_running = True
        self.day_thread.daemon = True
        self.day_thread.start()

        self.start_timer(5)

    def load_image(self):
        self.background_image = Image.open('assets/BgSiang.png')

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
            'command': "GET ACTION",
            'role': self.menu_manager.role,
            'name':self.menu_manager.name,
            'room_id': self.menu_manager.room_id,
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))
        print(f">> Send data to server: {send_data}")

        text = f"{name}({role})"
        self.name_role_text = tk.Label(self.background_canvas, text=text, foreground="#37342f", background='#ECE3D5',
                                       font=('Arial', 12))
        self.name_role_text.place(x=205, y=620)


        if self.menu_manager.role != "Peneliti":
            self.menu_manager.socket.send(pickle.dumps(send_data))

        self.timer_label = tk.Label(self.background_canvas, text='', foreground='#ECE3D5', background="#612C12",
                                    font=('Arial', 32))
        self.timer_label.place(x=1015, y=585)

    def update(self):
        while self.is_running:
            send_data = {
                'command': "GET ACTION",
                'role': self.menu_manager.role,
                'name': self.menu_manager.name,
                'room_id': self.menu_manager.room_id,
            }

            self.menu_manager.socket.send(pickle.dumps(send_data))

            # print(f">> Send data to server: {send_data}")
            try:
                data = self.menu_manager.socket.recv(2048)
                data = pickle.loads(data)
                print(data)

                if data["command"] == "RESPONSE ACTION":
                    self.menu_manager.game_info = data["game_info"]
                    if not data["game_info"]["players_killed"]:
                        text = "Tadi malam, Sukolilo terjaga dengan aman, tidak ada korban jiwa."
                    else:
                        length = len(data["game_info"]["players_killed"])
                        text = f"Telah ditemukan {length} mayat\n\n"

                        for player in data["game_info"]["players_killed"]:
                            text = text + f"{player} mati terbunuh\n"

                    self.text = tk.Label(self.background_canvas, text=text, foreground="#37342f", background='#ECE3D5', font=('Arial', 12))
                    self.text.place(x=445, y=350)
                    self.is_running = False
            except:
                pass

            time.sleep(2)

    def start_timer(self, seconds):
        self.remaining_time = seconds
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.configure(text=self.remaining_time)
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            self.is_running = False
            self.menu_manager.menus["chat"] = Chat(
                self.menu_manager, self.menu_manager)
            self.menu_manager.show_menu("chat")
