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
        self.create_profile()
        self.create_widgets()
        self.start_timer(8)

    def load_image(self):
        self.background_image = Image.open('assets/BgMalam.png')
        self.do_btn_image = Image.open('assets/button/Small Button Lakukan.png')
        self.hover_do_btn_image = Image.open('assets/button/Small Button Lakukan Hover.png')
        self.text_malam_1_image = Image.open('assets/TextMalam1.png')
        self.text_malam_2_image = Image.open('assets/TextMalam2.png')
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
    
    def create_profile(self):
        self.avatar_dead_image = Image.open('assets/AvatarDead.png')
        self.avatar_mahasiswa_image = Image.open('assets/AvatarMahasiswa.png')
        self.selected_avatar_mahasiswa_image = Image.open('assets/AvatarMahasiswaSelected.png')
        self.avatar_dokter_image = Image.open('assets/AvatarDokter.png')
        self.selected_avatar_dokter_image = Image.open('assets/AvatarDokterSelected.png')
        self.avatar_pemburu_image = Image.open('assets/AvatarPemburu.png')
        self.avatar_peneliti_image = Image.open('assets/AvatarPeneliti.png')
        self.avatar_werewolf_image = Image.open('assets/AvatarWerewolf.png')
        self.avatar_werewolf_dead_image = Image.open('assets/AvatarWerewolfDead.png')

        self.avatar_dead_photo = ImageTk.PhotoImage(self.avatar_dead_image)
        self.avatar_mahasiswa_photo = ImageTk.PhotoImage(self.avatar_mahasiswa_image)
        self.selected_avatar_mahasiswa_photo = ImageTk.PhotoImage(self.selected_avatar_mahasiswa_image)
        self.avatar_dokter_photo = ImageTk.PhotoImage(self.avatar_dokter_image)
        self.selected_avatar_dokter_photo = ImageTk.PhotoImage(self.selected_avatar_dokter_image)
        self.avatar_pemburu_photo = ImageTk.PhotoImage(self.avatar_pemburu_image)
        self.avatar_peneliti_photo = ImageTk.PhotoImage(self.avatar_peneliti_image)
        self.avatar_werewolf_photo = ImageTk.PhotoImage(self.avatar_werewolf_image)
        self.avatar_werewolf_dead_photo = ImageTk.PhotoImage(self.avatar_werewolf_dead_image)

        role = self.menu_manager.role

        player_avatars = []
        player_names = []

        data = self.menu_manager.game_info

        for count, player in enumerate(data["player_list"]):
            player_name = tk.Label(self.background_canvas, text=player['name'], background='#2A2545', foreground='#ECE3D5',
                                    font=('Arial', 12))
            
            if player['status'] == 'dead':
                if player['role'] == 'Werewolf':
                    avatar = tk.Label(self.background_canvas, image=self.avatar_werewolf_dead_photo, background='#50477D')
                else:
                    avatar = tk.Label(self.background_canvas, image=self.avatar_dead_photo, background='#50477D')
            elif role == "Werewolf" and player['role'] == "Werewolf":
                avatar = tk.Label(self.background_canvas, image=self.avatar_werewolf_photo, background='#50477D')
            elif role == "Peneliti" and player['role'] == "Peneliti":
                avatar = tk.Label(self.background_canvas, image=self.avatar_peneliti_photo, background='#50477D')
            elif role == "Pemburu" and player['role'] == "Pemburu":
                avatar = tk.Label(self.background_canvas, image=self.avatar_pemburu_photo, background='#50477D')
            elif role == "Dokter" and player['role'] == "Dokter":
                avatar = tk.Label(self.background_canvas, image=self.avatar_dokter_photo, background='#50477D')
            else:
                avatar = tk.Label(self.background_canvas, image=self.avatar_mahasiswa_photo, background='#50477D')

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
        role = self.menu_manager.role
        name = self.menu_manager.name

        role_card_path = 'assets/RoleCard' + role + '.png'
        self.role_card_image = Image.open(role_card_path)
        self.role_card_photo = ImageTk.PhotoImage(self.role_card_image)
        self.role_card = tk.Label(self.background_canvas, image=self.role_card_photo, background='#ECE3D5')

        if role == "Mahasiswa":
            self.text_malam = tk.Label(self.background_canvas, image=self.text_malam_2_photo, background='#ECE3D5')
            self.text_malam.place(x=444, y=183)
            self.role_card.place(x=540, y=282)
        else:
            self.text_malam = tk.Label(self.background_canvas, image=self.text_malam_1_photo, background='#ECE3D5')
            self.text_malam.place(x=312, y=183)
            self.role_card.place(x=344, y=282)

            self.player_subject = tk.StringVar(self)
            players_name = []
            data = self.menu_manager.game_info
            for player in data["player_list"]:
                if player['role'] != 'Dokter':
                    if player["status"] == "alive" and player["name"] != self.menu_manager.name and player["role"] != self.menu_manager.role:
                        players_name.append(player["name"])
                else:
                    players_name.append(player["name"])

            self.player_dropdown = ttk.OptionMenu(
                self, self.player_subject, *players_name)
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

    def action(self):
        player_name = self.player_subject.get()

        send_data = {
            'command': "ACTION",
            'room_id': self.menu_manager.room_id,
            'role': self.menu_manager.role,
            'player_name': self.menu_manager.name,
            'action_subject': player_name,
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))

        print(f">> Send data to server: {send_data}")

        role = self.menu_manager.role
        
        self.role_card.place(x=540, y=282)
        self.text_malam.destroy()
        self.do_button.destroy()
        self.player_dropdown.destroy()

        if role == "Peneliti":
            for player in self.menu_manager.game_info['player_list']:
                if player['name'] == self.player_subject.get():
                    target_role = player['role']
                    break

            text = f"{self.player_subject.get()} adalah seorang {target_role}"
            role_card_path = 'assets/RoleCard' + target_role + '.png'
            self.role_card_image = Image.open(role_card_path)
            self.role_card_photo = ImageTk.PhotoImage(self.role_card_image)
            self.role_card.configure(image=self.role_card_photo)
        elif role == "Werewolf" or role == "Pemburu":
            text = f"Anda akan membunuh {self.player_subject.get()}"
        elif role == "Dokter":
            text = f"{self.player_subject.get()} telah mendapatkan perlindunggan Anda"
        
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
            send_data = {
                'command': "GET NIGHT RESULT",
                'name': self.menu_manager.name,
                'room_id': self.menu_manager.room_id,
            }

            print(f">> Send data to server: {send_data}")

            self.menu_manager.socket.send(pickle.dumps(send_data))

            is_receiving = True

            while is_receiving:
                data = self.menu_manager.socket.recv(2048)
                data = pickle.loads(data)

                if data['command'] == "NIGHT RESULT": 
                    is_receiving = False

            self.menu_manager.game_info = data["game_info"]

            print(data)

            self.menu_manager.menus["day"] = Day(
                self.menu_manager, self.menu_manager)
            self.menu_manager.show_menu("day")




