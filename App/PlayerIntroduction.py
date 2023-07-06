import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from App.WelcomeGame import WelcomeGame

class PlayerIntroduction(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_widgets()
        self.start_timer(1)


    def load_image(self):
        self.background_image = Image.open(f'assets/BgPlayerIntroduction{self.menu_manager.team}{self.menu_manager.num_players}.png')
        self.background_photo = ImageTk.PhotoImage(self.background_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.menu_manager.screen_width, height=self.menu_manager.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)

    def create_widgets(self):
        player_names = []
        player_count = 0

        if self.menu_manager.team == "Warga":
            for count, player in enumerate(self.menu_manager.game_info["player_list"]):
                if self.menu_manager.num_players == '4':
                    player_name = tk.Label(self.background_canvas, text=player['name'], background='#2A2545', foreground='#ECE3D5',
                                    font=('Arial', 16))
                    player_name.place(x=275+191*player_count, y=570)
                elif self.menu_manager.num_players == '8':
                    player_name = tk.Label(self.background_canvas, text=player['name'], background='#2A2545', foreground='#ECE3D5',
                                        font=('Arial', 16))
                    if count < 4:
                        player_name.place(x=87+139*player_count, y=494)
                    else:
                        player_name.place(x=100+139*player_count, y=401)
                elif self.menu_manager.num_players == '12':
                    player_name = tk.Label(self.background_canvas, text=player['name'], background='#2A2545', foreground='#ECE3D5',
                                        font=('Arial', 16))
                    if count < 3:
                        player_name.place(x=261+122*player_count, y=452)
                    elif count < 6:
                        player_name.place(x=261+122*(player_count%3), y=643)
                    elif count < 9:
                        player_name.place(x=685+122*(player_count%3), y=452)
                    else:
                        player_name.place(x=685+122*(player_count%3), y=643)

                player_names.append(player_name)
                player_count += 1
        else:
            for count, player in enumerate(self.menu_manager.game_info["player_list"]):
                if player['role'] == 'Werewolf':
                    if self.menu_manager.num_players == '4':
                        if player_count < 1:
                            player_name = tk.Label(self.background_canvas, text=player['name'], background='#2A2545', foreground='#ECE3D5',
                                        font=('Arial', 16))
                            player_name.place(x=559, y=570)
                    elif self.menu_manager.num_players == '8':
                        if player_count < 2:
                            player_name = tk.Label(self.background_canvas, text=player['name'], background='#2A2545', foreground='#ECE3D5',
                                        font=('Arial', 16))
                            player_name.place(x=456+player_count*212, y=570)
                    elif self.menu_manager.num_players == '12':
                        if player_count < 3:
                            player_name = tk.Label(self.background_canvas, text=player['name'], background='#2A2545', foreground='#ECE3D5',
                                        font=('Arial', 16))
                            player_name.place(x=349+player_count*212, y=570)
                        
                    player_names.append(player_name)
                    player_count += 1


        self.timer_label = tk.Label(self.background_canvas, text='', foreground='#ECE3D5', background="#2A2545", font=('Arial', 32))
        self.timer_label.place(x=1215, y=30)

    def start_timer(self, seconds):
        self.remaining_time = seconds
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.configure(text=self.remaining_time)
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            self.menu_manager.menus["welcome_game"] = WelcomeGame(
                self.menu_manager, self.menu_manager)
            self.menu_manager.show_menu("welcome_game")

