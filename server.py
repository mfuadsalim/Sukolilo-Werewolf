import select
import socket
import sys
import threading
import pickle

client_sockets = []
rooms = {}
players_socket = []


class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []
        print(
            f"The Sukolilo Werewolf server is starting on {self.host} port {self.port}\n")

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

            if (data['command'] == "CREATE ROOM"):
                self.create_room(data, self.client)

            if (data['command'] == "GET DETAIL ROOM"):
                self.get_detail_room(data)

            if (data['command'] == "JOIN ROOM"):
                self. join_room(data, self.client)

            if data['command'] == "CHECK ROOM":
                self.check_room(data)

    def create_room(self, data, client):
        room_id = data['room_id']
        rooms[room_id] = {"num_players": None, "player_list": []}
        rooms[room_id]["num_players"] = data['num_players']
        print(
            f'>> {data["name"]} CREATE ROOM room_id={room_id} num players={data["num_players"]}')

        self.join_room(data, client)

    def get_detail_room(self, data):
        room_id = data["room_id"]
        self.client.send(pickle.dumps(rooms[room_id]))

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
            players_socket.append(player_socket)

            print(f'>>{data["name"]} JOIN ROOM with id: {room_id}')
            print(f'>> server ROOM DETAILS={rooms}')
            print(f'>> server SOCKET DETAILS={players_socket}')

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


if __name__ == "__main__":
    s = Server()
    s.run()
