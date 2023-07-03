import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pickle
import threading

from App.Day import Day


class Night(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_widgets()

        self.night_thread = threading.Thread(target=self.update)
        self.is_running = True
        # Set the thread as a daemon to stop it when the main thread exits
        self.night_thread.daemon = True
        self.night_thread.start()

        self.start_timer(15)

    def load_image(self):
        self.background_image = Image.open('assets/BgMalam.png')
        self.do_btn_image = Image.open('assets/button/Small Button Lakukan.png')
        self.hover_do_btn_image = Image.open('assets/button/Small Button Lakukan Hover.png')
        self.text_malam_1_image = Image.open('assets/TextMalam1.png')
        self.text_malam_2_image = Image.open('assets/TextMalam2.png')

        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.do_btn_photo = ImageTk.PhotoImage(self.do_btn_image)
        self.hover_do_btn_photo = ImageTk.PhotoImage(self.hover_do_btn_image)
        self.text_malam_1_photo = ImageTk.PhotoImage(self.text_malam_1_image)
        self.text_malam_2_photo = ImageTk.PhotoImage(self.text_malam_2_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.menu_manager.screen_width, height=self.menu_manager.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)

    def create_widgets(self):
        role = self.menu_manager.role
        name = self.menu_manager.name

        role_card_path = 'assets/RoleCard' + role + '.png'
        self.role_card_image = Image.open(role_card_path)
        self.role_card_photo = ImageTk.PhotoImage(self.role_card_image)
        self.role_card = tk.Label(self.background_canvas, image=self.role_card_photo, background='#ECE3D5')

        text = f"{name}({role})"
        self.name_role_text = tk.Label(self.background_canvas, text=text, foreground="#37342f", background='#ECE3D5',
                             font=('Arial', 12))
        self.name_role_text.place(x=286, y=578)

        if role == "Mahasiswa":
            self.text_malam = tk.Label(self.background_canvas, image=self.text_malam_2_photo, background='#ECE3D5')
            self.text_malam.place(x=444, y=183)
            self.role_card.place(x=540, y=282)
        else:
            self.text_malam = tk.Label(self.background_canvas, image=self.text_malam_1_photo, background='#ECE3D5')
            self.text_malam.place(x=312, y=183)
            self.role_card.place(x=344, y=282)

            self.player = tk.StringVar(self)
            players_name = []
            data = self.menu_manager.game_info
            for player in data["player_list"]:
                if player["status"] == "alive" and player["name"] != self.menu_manager.name:
                    players_name.append(player["name"])

            self.player_dropdown = ttk.OptionMenu(
                self, self.player, *players_name)
            self.player_dropdown.place(x=740, y=360)

            self.do_button = tk.Button(
                self.background_canvas, image=self.do_btn_photo, command=self.action, borderwidth=0)
            self.do_button.place(x=696, y=421)
            self.do_button.bind('<Enter>', lambda event: self.do_button.config(
                image=self.hover_do_btn_photo))
            self.do_button.bind('<Leave>', lambda event: self.do_button.config(
                image=self.do_btn_photo))

        self.timer_label = tk.Label(self.background_canvas, text='', foreground='#ECE3D5', background="#4f4960",
                                    font=('Arial', 32))
        self.timer_label.place(x=945, y=550)

    def update(self):
        role = self.menu_manager.role
        while self.is_running:
            try:
                if role != "Mahasiswa":
                    data = self.menu_manager.socket.recv(2048)
                    data = pickle.loads(data)
                    print(f">> Send data to server: {data}")
                    if data["command"] == "RESPONSE ACTION":
                        self.subject_role = data["role"]
                        self.is_running = False
                    elif data["command"] == "None":
                        self.is_running = False
            except:
                pass

    def action(self):
        player_name = self.player.get()

        send_data = {
            'command': "ACTION",
            'room_id': self.menu_manager.room_id,
            'role': self.menu_manager.role,
            'player_name': self.menu_manager.name,
            'action_subject': player_name,
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))
        print(f'>> Send data to server: {send_data}')

        role = self.menu_manager.role
        if role == "Mahasiswa":
            pass
        else:
            self.role_card.place(x=540, y=282)
            self.text_malam.destroy()
            self.do_button.destroy()
            self.player_dropdown.destroy()
            if role == "Peneliti":
                text = f"{self.player.get()} adalah seorang {self.subject_role}"
                role_card_path = 'assets/RoleCard' + self.subject_role + '.png'
                self.role_card_image = Image.open(role_card_path)
                self.role_card_photo = ImageTk.PhotoImage(self.role_card_image)
                self.role_card.configure(image=self.role_card_photo)
            elif role == "Werewolf" or role == "Hunter":
                text = f"Anda berhasil membunuh {self.player.get()}"

            text_after_act = tk.Label(self.background_canvas, text=text, background='#ECE3D5',
                                      font=('Arial', 12))
            text_after_act.place(x=520, y=230)

    def start_timer(self, seconds):
        self.remaining_time = seconds
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.configure(text=self.remaining_time)
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            self.menu_manager.menus["day"] = Day(
                self.menu_manager, self.menu_manager)
            self.menu_manager.show_menu("day")




