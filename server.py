import select
import socket
import sys
import threading
import pickle
import random

client_sockets = []
rooms = {
    '123456': {
        'num_players': '4',
        'player_list': [
            {'name': 'Isol', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False},
            {'name': 'Fuad', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False},
            {'name': 'Monica', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False},
        ],
        'players_killed': []
    }
}
players_socket = {
    '123456': []
}


class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []
        print(
            "============================================================================")
        print(
            f"The Sukolilo Werewolf server is starting on {self.host} port {self.port}")
        print(
            "============================================================================\n")

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

    def run(self):
        self.open_socket()
        input = [self.server]
        running = 1
        while running:
            inputready, outputready, exceptready = select.select(input, [], [])

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    client_socket, client_address = self.server.accept()
                    print(
                        f">> New client connected to server: {client_address}")
                    client_sockets.append(client_socket)
                    c = Client(client_socket, client_address)
                    c.start()
                    self.threads.append(c)
                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

        # close all threads
        self.server.close()
        for c in self.threads:
            c.join()


class Client(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            data = pickle.loads(data)

            if data['command'] == "CREATE ROOM":
                self.create_room(data, self.client)

            if data['command'] == "GET DETAIL ROOM":
                self.get_detail_room(data)

            if data['command'] == "JOIN ROOM":
                self.join_room(data, self.client)

            if data['command'] == "CHECK ROOM":
                self.check_room(data)

            if data['command'] == "GENERATE AVATAR":
                self.generate_avatar(data)

            if data['command'] == "ACTION":
                self.action(data)

            if data['command'] == "GET ACTION":
                self.get_action(data)

            if data['command'] == "CHAT":
                self.chat(data)

    def create_room(self, data, client):
        room_id = data['room_id']
        rooms[room_id] = {"num_players": None, "player_list": [], "players_killed": []}
        players_socket[room_id] = []
        rooms[room_id]["num_players"] = data['num_players']
        print(
            f'>> {data["name"]} CREATE ROOM room_id={room_id} num players={data["num_players"]}')

        self.join_room(data, client)

    def get_detail_room(self, data):
        room_id = data["room_id"]
        send_data = {
            'command': 'GET DETAIL ROOM',
            'game_info': rooms[room_id]
        }
        self.client.send(pickle.dumps(send_data))

    def join_room(self, data, client):
        room_id = data['room_id']
        if room_id in rooms:
            player_details = {
                "name": data['name'],
                "role": "",
                "status": "alive",
                "has_voted": False,
                "has_acted": False
            }
            rooms[room_id]["player_list"].append(player_details)

            player_socket = {
                "name": data['name'],
                "socket": client
            }
            players_socket[room_id].append(player_socket)

            print(f'>> {data["name"]} JOIN ROOM with id: {room_id}')
            # print(f'>> server ROOM DETAILS={rooms}')
            # print(f'>> server SOCKET DETAILS={players_socket}')

    def check_room(self, data):
        room_id = data['room_id']
        send_data = {
            'status': ''
        }
        if room_id in rooms:
            send_data['status'] = 'EXIST'
        else:
            send_data['status'] = 'DOES NOT EXIST'
        self.client.send(pickle.dumps(send_data))

        print(
            f'>> {data["name"]} CHECK ROOM room_id={room_id} -> status={send_data["status"]}')

    def generate_avatar(self, data):
        room_id = data["room_id"]
        num_players = int(rooms[room_id]["num_players"])
        avatars = []
        if num_players == 4:
            avatars = ['Werewolf', 'Peneliti', 'Mahasiswa', 'Mahasiswa']
            # avatars = ['Peneliti', 'Peneliti', 'Peneliti', 'Peneliti']
        elif num_players == 8:
            avatars = ['Werewolf', 'Werewolf', 'Peneliti', 'Pemburu',
                       'Mahasiswa', 'Mahasiswa', 'Mahasiswa', 'Mahasiswa']
        elif num_players == 12:
            avatars = ['Werewolf', 'Werewolf', 'Werewolf', 'Peneliti', 'Peneliti', 'Pemburu',
                       'Mahasiswa', 'Mahasiswa', 'Mahasiswa', 'Mahasiswa', 'Mahasiswa', 'Mahasiswa']

        random.shuffle(avatars)

        # Perform start game logic with avatars here
        for i, player in enumerate(rooms[room_id]['player_list']):
            avatar = avatars[i]
            rooms[room_id]['player_list'][i]['role'] = avatar

        send_data = {
            'command': 'START GAME',
            'game_info': rooms[room_id]
        }
        print(f'>> {room_id} server Game Start')
        self.broadcast(send_data, room_id)

    def action(self, data):
        room_id = data["room_id"]

        if data["role"] == "Werewolf" or data["role"] == "Hunter":
            send_data = {
                'command': 'None'
            }
            self.client.send(pickle.dumps(send_data))

            if data["action_subject"] in rooms[room_id]["players_killed"]:
                pass
            else:
                rooms[room_id]["players_killed"].append(data["action_subject"])
                for player in rooms[room_id]['player_list']:
                    if player['name'] == data["action_subject"]:
                        player['status'] = 'dead'
                print(f">> {room_id} {data['player_name']}({data['role']}) kill {data['action_subject']}")

        elif data["role"] == "Peneliti":
            role = None
            for player in rooms[room_id]['player_list']:
                if player['name'] == data["action_subject"]:
                    role = player['role']
            send_data = {
                'command': 'RESPONSE ACTION',
                'role': role
            }
            self.client.send(pickle.dumps(send_data))
            print(f">> {room_id} {data['player_name']}({data['role']}) seek for {data['action_subject']}'s role={role}")

    def get_action(self, data):
        room_id = data["room_id"]
        game_info = rooms[room_id]
        send_data = {
            'command': 'RESPONSE ACTION',
            'game_info': game_info
        }
        print(f"{room_id} {data['name']}({data['role']}) GET ACTION: {send_data}")
        self.client.send(pickle.dumps(send_data))

    def chat(self, data):
        room_id = data["room_id"]
        message = f"{data['name']}\t: {data['message']}"
        send_data = {
            'command': "RESPONSE CHAT",
            'chat_messages': message
        }
        print(f"{room_id} {data['name']}({data['role']}) Chat: {data['message']}")
        self.broadcast(send_data, room_id)

    def broadcast(self, send_data, room_id):
        for player in players_socket[room_id]:
            player_socket = player["socket"]
            player_socket.send(pickle.dumps(send_data))


if __name__ == "__main__":
    s = Server()
    s.run()
