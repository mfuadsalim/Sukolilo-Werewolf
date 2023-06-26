import select
import socket
import sys
import threading
import pickle

client_sockets = []
rooms = {}
players = {}

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []
        print("-- Server Start --")

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(5)

    def run(self):
        self.open_socket()
        input = [self.server]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    client_socket, client_address = self.server.accept()
                    print(f"{client_address} connected to server")
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
        print(client_sockets)
        print(f'address: {self.address}')

        while running:
            data = self.client.recv(self.size)
            data = pickle.loads(data)
 
            if (data['command'] == "CREATE ROOM"):
                room_id = data['room_id']
                rooms[room_id] = {"num_players": [], "player_list": []}
                rooms[room_id]["num_players"].append(data['players'])
                rooms[room_id]["player_list"].append(data['name'])
                print(f'{data["name"]} CREATE ROOM with room id: {room_id} and num players: {data["players"]}')
                print(f'ROOM Detail: {rooms}')

            if (data['command'] == "GET DETAIL ROOM"):
                send_data = rooms[data['room_id']]
                print(f'{data["name"]} GET DETAIL ROOM: {send_data}')
                self.client.send(pickle.dumps(send_data))

            if (data['command'] == "JOIN ROOM"):
                room_id = data['room_id']
                if room_id in rooms:
                    rooms[room_id]["player_list"].append(data['name'])
                    print(f'{data["name"]} JOIN ROOM with id: {room_id}')
                    print(f'ROOM Detail: {rooms}')

            if data['command'] == "CHECK ROOM":
                room_id = data['room_id']
                
                send_data = {
                    'status' : ''
                }

                if room_id in rooms:
                    send_data['status'] = 'EXIST'
                else:
                    send_data['status'] = 'DOES NOT EXIST'

                self.client.send(pickle.dumps(send_data))
            
            if (data['command'] == "CHECK ROOM ID"):
                send_data = {
                    'status' : ''
                }

                if data['room_id'] in rooms:
                    send_data['status'] = 'ROOM ID EXIST'
                else:
                    send_data['status'] = 'ROOM ID DOES NOT EXIST'
                
                self.client.send(pickle.dumps(send_data))


if __name__ == "__main__":
    s = Server()
    s.run()