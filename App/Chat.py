import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import pickle
import threading
import time

from App.Vote import Vote


class Chat(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.load_image()
        self.create_canvas()
        self.create_profile()
        self.create_widgets()
        self.chat_messages = []
        self.chat_thread = threading.Thread(target=self.update)
        self.is_running = True
        # Set the thread as a daemon to stop it when the main thread exits
        self.chat_thread.daemon = True
        self.chat_thread.start()

        self.start_timer(3)

    def load_image(self):
        self.background_image = Image.open('assets/BgChat.png')
        self.submit_btn_image = Image.open('assets/button/Small Button Kirim.png')
        self.hover_submit_btn_image = Image.open('assets/button/Small Button Kirim Hover.png')
        self.disabled_submit_btn_image = Image.open('assets/button/Small Disabled Button Kirim.png')

        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.submit_btn_photo = ImageTk.PhotoImage(self.submit_btn_image)
        self.hover_submit_btn_photo = ImageTk.PhotoImage(self.hover_submit_btn_image)
        self.disabled_submit_btn_photo = ImageTk.PhotoImage(self.disabled_submit_btn_image)

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
        role = self.menu_manager.role
        name = self.menu_manager.name

        # Create the chat display text box
        self.chat_display = tk.Text(self.background_canvas, height=12, width=57, foreground="#37342f", background='#ECE3D5', font=('Arial', 16))
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.place(x=295, y=183)

        # Create the chat entry
        self.chat_entry = tk.Entry(self.background_canvas, width=76, foreground="#37342f", background='#ECE3D5', font=('Arial', 12))
        self.chat_entry.focus_set()
        self.chat_entry.place(x=295, y=520)

        # Create the submit button
        if self.menu_manager.status == 'dead':
            self.submit_button = tk.Label(self.background_canvas, image=self.disabled_submit_btn_photo, text="")
            self.submit_button.place(x=590, y=580)
        elif self.menu_manager.status == 'alive':
            self.submit_button = tk.Button(
                self.background_canvas, image=self.submit_btn_photo, command=self.submit_chat, borderwidth=0)
            self.submit_button.bind('<Enter>', lambda event: self.submit_button.config(
                image=self.hover_submit_btn_photo))
            self.submit_button.bind('<Leave>', lambda event: self.submit_button.config(
                image=self.submit_btn_photo))
            self.submit_button.place(x=590, y=580)

        self.timer_label = tk.Label(self.background_canvas, text='', foreground='#ECE3D5', background="#612C12", font=('Arial', 32))
        self.timer_label.place(x=950, y=590)

    def update(self):
        while self.is_running:
            try:
                data = self.menu_manager.socket.recv(2048)
                data = pickle.loads(data)
                print(data)

                if data["command"] == "RESPONSE CHAT":
                    self.chat_messages.append(data["chat_messages"])

                # Update the chat display
                self.update_chat_display()
            except:
                pass

    def submit_chat(self):
        # Get the chat message from the chat entry
        message = self.chat_entry.get()

        # Clear the chat entry
        self.chat_entry.delete(0, tk.END)

        send_data = {
            'command': "CHAT",
            'name': self.menu_manager.name,
            'room_id': self.menu_manager.room_id,
            'role': self.menu_manager.role,
            'message': message
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))
        print(f">> Chat: {message}")



    def update_chat_display(self):
        # Set the state of the chat display to normal
        self.chat_display.config(state=tk.NORMAL)

        # Clear the chat display
        self.chat_display.delete(1.0, tk.END)

        # Display the latest chat messages in the correct order (top to bottom)
        start_index = max(0, len(self.chat_messages) - 15)  # Limit the display to 15 messages
        chat_messages_to_display = self.chat_messages[start_index:]

        # Insert the chat messages into the chat display
        for message in chat_messages_to_display:
            self.chat_display.insert(tk.END, message + "\n")

        # Set the state of the chat display back to disabled
        self.chat_display.config(state=tk.DISABLED)

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
            self.chat_messages = []

            self.menu_manager.menus["vote"] = Vote(
                self.menu_manager, self.menu_manager)
            self.menu_manager.show_menu("vote")