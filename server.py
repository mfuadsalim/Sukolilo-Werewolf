import select
import socket
import sys
import threading
import pickle
import random
from collections import Counter

client_sockets = []
rooms = {
    '123456': {
        'num_players': '4',
        'player_list': [
            {'name': 'Isol', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Fuad', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Monica', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
        ]
    },
    '234567': {
        'num_players': '8',
        'player_list': [
            {'name': 'Isol', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Isol2', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Isol3', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Isol4', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Isol5', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Fuad', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Monica', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
        ]
    },
    '345678': {
        'num_players': '12',
        'player_list': [
            {'name': 'Isol', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Isol2', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Isol3', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Isol4', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Isol5', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Isol6', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Isol7', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Isol8', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Isol9', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Fuad', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
            {'name': 'Monica', 'role': '', 'status': 'alive',
                'has_voted': False, 'has_acted': False, 'is_ready': True},
        ]
    },
    '444': {
        'num_players': '4',
        'player_list': []
    }
}
players_socket = {
    '123456': [],
    '234567': [],
    '345678': [],
    '444': []
}

players_voted = {
    '123456': [],
    '234567': [],
    '345678': [],
    '444': []
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
            f"Sukolilo Werewolf server is starting on {self.host} port {self.port}")
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
        print(f'address: {self.address}')

        while running:
            try:
                data = self.client.recv(self.size)
                data = pickle.loads(data)

                if (data['command'] == "CREATE ROOM"):
                    self.create_room(data, self.client)

                if (data['command'] == "GET DETAIL ROOM"):
                    self.get_detail_room(data)

                if (data['command'] == "JOIN ROOM"):
                    self. join_room(data, self.client)

                if data['command'] == "CHECK ROOM":
                    self.check_room(data)

                if (data['command'] == "CHECK ROOM ID"):
                    self.check_room_id(data)

                if (data['command'] == "PLAYER READY"):
                    self.player_ready(data)

                if data['command'] == "GENERATE AVATAR":
                    self.generate_avatar(data)

                if data['command'] == "ACTION":
                    self.action(data)

                if data['command'] == "GET NIGHT RESULT":
                    self.get_night_result(data)
                
                if data['command'] == "SUMMARIZE NIGHT":
                    self.summarize_night(data)

                if data['command'] == "CHAT":
                    self.chat(data)

                if data['command'] == "VOTE":
                    self.vote(data)

                if data['command'] == "VOTE RESULT":
                    self.vote_result(data)

            except ConnectionResetError as e:
                if "WinError 10054" in str(e):
                    player_name = ""
                    for room_id, player_list in players_socket.items():
                        for player in player_list:
                            if (player["socket"] == self.client):
                                player_name = player["name"]
                                player_list.remove(player)

                        for player in rooms[room_id]["player_list"]:
                            if (player["name"] == player_name):
                                rooms[room_id]["player_list"].remove(player)

                    print("Connection forcibly closed by the remote host")
                    running = 0
                else:
                    raise e

    def create_room(self, data, client):
        room_id = data['room_id']
        rooms[room_id] = {"num_players": None, "player_list": []}
        players_socket[room_id] = []
        players_voted[room_id] = []
        rooms[room_id]["num_players"] = data['num_players']
        print(
            f'>> {data["name"]} CREATE ROOM room_id={room_id} num players={data["num_players"]}')

        self.join_room(data, client)

    def get_detail_room(self, data):
        room_id = data["room_id"]
        send_data = {
            'command': 'GET DETAIL ROOM',
            'game_info': rooms[room_id],
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
                "has_acted": False,
                "is_ready": False
            }
            rooms[room_id]["player_list"].append(player_details)

            player_socket = {
                "name": data['name'],
                "socket": client
            }
            players_socket[room_id].append(player_socket)

            print(f'>> {data["name"]} JOIN ROOM with id: {room_id}')

    def check_room(self, data):
        room_id = data['room_id']
        send_data = {
            'status': ''
        }
        if room_id in rooms:
            room_num = int(rooms[room_id]["num_players"])
            if (len(rooms[room_id]["player_list"]) >= room_num):
                send_data['status'] = 'FULL'
            else:
                send_data['status'] = 'EXIST'
        else:
            send_data['status'] = 'DOES NOT EXIST'
        self.client.send(pickle.dumps(send_data))

        print(
            f'>> {data["name"]} CHECK ROOM room_id={room_id} -> status={send_data["status"]}')

    def check_room_id(self, data):
        send_data = {
            'status' : ''
        }

        if data['room_id'] in rooms:
            send_data['status'] = 'ROOM ID EXIST'
        else:
            send_data['status'] = 'ROOM ID DOES NOT EXIST'

        self.client.send(pickle.dumps(send_data))

    def player_ready(self, data):
        room_id = data["room_id"]
        player_list = rooms[room_id]["player_list"]

        for player in player_list:
            if (player["name"] == data["name"]):
                player["is_ready"] = True

        print(
            f'>> a PLAYER READY with name={data["name"]} and room_id={room_id}')

    def generate_avatar(self, data):
        room_id = data["room_id"]
        num_players = int(rooms[room_id]["num_players"])
        avatars = []
        if num_players == 4:
            # avatars = ['Werewolf', 'Peneliti', 'Mahasiswa', 'Mahasiswa']
            avatars = ['Werewolf', 'Pemburu', 'Pemburu', 'Pemburu']
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

        if data["role"] == "Werewolf" or data["role"] == "Pemburu":
            for player in rooms[room_id]['player_list']:
                if player['name'] == data["action_subject"]:
                    if player['status'] != 'protected':
                        player['status'] = 'dying'
                    else:
                        player['status'] = 'dispelled'
            print(f">> {room_id} {data['player_name']}({data['role']}) kill {data['action_subject']}")

        elif data["role"] == "Peneliti":
            role = None
            for player in rooms[room_id]['player_list']:
                if player['name'] == data["action_subject"]:
                    role = player['role']

            print(f">> {room_id} {data['player_name']}({data['role']}) seek for {data['action_subject']}'s role={role}")

        elif data["role"] == "Dokter":
            for player in rooms[room_id]['player_list']:
                if player['name'] == data["action_subject"]:
                    if player['status'] != 'dying':
                        player['status'] = 'protected'
                    else:
                        player['status'] = 'dispelled'
            print(f">> {room_id} {data['player_name']}({data['role']}) protect {data['action_subject']}")
        

    def get_night_result(self, data):
        room_id = data["room_id"]
        game_info = rooms[room_id]

        send_data = {
            'command': 'NIGHT RESULT',
            'game_info': game_info
        }
        print(f">> {room_id} {data['name']} GET NIGHT RESULT: {send_data}")
        self.client.send(pickle.dumps(send_data))

    def summarize_night(self, data):
        room_id = data["room_id"]

        for player in rooms[room_id]['player_list']:
            if player['status'] == 'dying':
                player['status'] = 'dead'
            if player['status'] == 'dispelled' or player['status'] == 'protected':
                player['status'] = 'alive'
        
        send_data = {
            'command': 'SUMMARIZED NIGHT',
            'game_info': rooms[room_id]
        }
        
        print(f">> {data['name']} SUMMARIZED NIGHT")
        self.client.send(pickle.dumps(send_data))

    def chat(self, data):
        room_id = data["room_id"]
        players_voted[room_id] = []

        message = f"{data['name']}\t: {data['message']}"
        send_data = {
            'command': "RESPONSE CHAT",
            'chat_messages': message
        }
        print(f">> {room_id} {data['name']}({data['role']}) Chat: {data['message']}")
        self.broadcast(send_data, room_id)

    def vote(self, data):
        room_id = data["room_id"]

        players_voted[room_id].append(data["player_voted"])

        print(f">> {room_id} {data['name']}({data['role']}) Voted for: {data['player_voted']}")

    def vote_result(self, data):
        room_id = data["room_id"]
        player_list = rooms[room_id]["player_list"]

        vote_counts = Counter(players_voted[room_id])
        most_common = vote_counts.most_common(2)

        if len(most_common) == 1 or (len(most_common) > 1 and most_common[0][1] > most_common[1][1]):
            for player in player_list:
                if player["name"] == most_common[0][0]:
                    player["status"] = 'dead'

            vote_result = most_common[0][0]
            voted_role = next((player["role"] for player in player_list if player["name"] == vote_result), None)
        else:
            vote_result = None
            voted_role = None

        send_data = {
            'command' : "RESPONSE VOTE RESULT",
            'game_info' : rooms[room_id],
            'vote_result' : vote_result,
            'voted_role': voted_role
        }

        print(f">> {room_id} {data['name']} Get vote result: {send_data['vote_result']}")

        self.client.send(pickle.dumps(send_data))



    def broadcast(self, send_data, room_id):
        for player in players_socket[room_id]:
            player_socket = player["socket"]
            player_socket.send(pickle.dumps(send_data))


if __name__ == "__main__":
    s = Server()
    s.run()
