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
        self.create_widgets()
        self.chat_messages = []
        self.chat_thread = threading.Thread(target=self.update)
        self.is_running = True
        # Set the thread as a daemon to stop it when the main thread exits
        self.chat_thread.daemon = True
        self.chat_thread.start()

        self.start_timer(30)

    def load_image(self):
        self.background_image = Image.open('assets/BgChat.png')
        self.submit_btn_image = Image.open('assets/button/Small Button Kirim.png')
        self.hover_submit_btn_image = Image.open('assets/button/Small Button Kirim Hover.png')

        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.submit_btn_photo = ImageTk.PhotoImage(self.submit_btn_image)
        self.hover_submit_btn_photo = ImageTk.PhotoImage(self.hover_submit_btn_image)

    def create_canvas(self):
        self.background_canvas = tk.Canvas(
            self, width=self.menu_manager.screen_width, height=self.menu_manager.screen_height)
        self.background_canvas.pack()
        self.background_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)

    def create_widgets(self):
        role = self.menu_manager.role
        name = self.menu_manager.name

        # Create the chat display text box
        self.chat_display = tk.Text(self.background_canvas, height=15, width=70, foreground="#37342f", background='#ECE3D5', font=('Arial', 16))
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.place(x=217, y=183)

        # Create the chat entry
        self.chat_entry = tk.Entry(self.background_canvas, width=93, foreground="#37342f", background='#ECE3D5', font=('Arial', 12))
        self.chat_entry.focus_set()
        self.chat_entry.place(x=218, y=567)

        # Create the submit button
        self.submit_button = tk.Button(
            self.background_canvas, image=self.submit_btn_photo, command=self.submit_chat, borderwidth=0)
        self.submit_button.place(x=696, y=421)
        self.submit_button.bind('<Enter>', lambda event: self.submit_button.config(
            image=self.hover_submit_btn_photo))
        self.submit_button.bind('<Leave>', lambda event: self.submit_button.config(
            image=self.submit_btn_photo))
        self.submit_button.place(x=590, y=602)

        text = f"{name}({role})"
        self.name_role_text = tk.Label(self.background_canvas, text=text, foreground="#37342f", background='#ECE3D5',
                                       font=('Arial', 12))
        self.name_role_text.place(x=205, y=620)

        self.timer_label = tk.Label(self.background_canvas, text='', foreground='#ECE3D5', background="#612C12",
                                    font=('Arial', 32))
        self.timer_label.place(x=1015, y=585)

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