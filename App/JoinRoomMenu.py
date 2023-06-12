import tkinter as tk
from tkinter import ttk
import pickle
import tkinter.messagebox as messagebox


from App.WaitingRoom import WaitingRoom

class JoinRoomMenu(tk.Frame):
    def __init__(self, master, menu_manager):
        super().__init__(master)
        self.menu_manager = menu_manager
        self.create_widgets()

    def create_widgets(self):
        name_label = ttk.Label(self, text="Name:")
        name_label.pack()
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack()

        code_label = ttk.Label(self, text="Room Code:")
        code_label.pack()
        self.code_entry = ttk.Entry(self)
        self.code_entry.pack()

        join_button = ttk.Button(self, text="Join Room", command=self.join_room)
        join_button.pack()

        back_button = ttk.Button(self, text="Back to Menu", command=self.menu_manager.show_main_menu)
        back_button.pack()

    def join_room(self):
        name = self.name_entry.get()
        room_code = self.code_entry.get()
        # Code for joining a room goes here
        # You can update the window or perform any other actions
        self.menu_manager.name = name
        print(f'Set player name to: {self.menu_manager.name}')

        self.menu_manager.room_id = room_code
        print(f'Set room id to: {self.menu_manager.room_id}')


        send_data = {
            'command' : "CHECK ROOM",
            'room_id' : room_code,
            'name'    : name,
        }

        self.menu_manager.socket.send(pickle.dumps(send_data))
        print(f'Send data to server: {send_data}')

        data = self.menu_manager.socket.recv(2048)
        data = pickle.loads(data)

        if data['status'] == 'DOES NOT EXIST':
            messagebox.showerror("Error", "Room does not exist.")
        else:
            send_data = {
                'command' : "JOIN ROOM",
                'room_id' : room_code,
                'name'    : name,
            }

            self.menu_manager.socket.send(pickle.dumps(send_data))
            print(f'Send data to server: {send_data}')

            self.menu_manager.menus["waiting_room"] = WaitingRoom(self.menu_manager, self.menu_manager)
            self.menu_manager.show_menu("waiting_room")
