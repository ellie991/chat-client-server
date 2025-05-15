import socket
from threading import Thread

class Server:
    Clients = []

    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        print('Server waiting for connections...')

    def listen(self):
        while True:
            client_socket, address = self.socket.accept()
            print("Connection from:", address)

            data = client_socket.recv(1024).decode()
            name, udp_port = data.split("|")
            client = {
                'client_name': name,
                'client_socket': client_socket,
                'connected_client': None,
                'udp_address': (address[0], int(udp_port))
            }

            self.broadcast_message(name, f"{name} has joined the chat!")
            Server.Clients.append(client)
            Thread(target=self.handle_new_client, args=(client,)).start()

    def handle_new_client(self, client):
        name = client['client_name']
        sock = client['client_socket']

        while True:
            try:
                msg = sock.recv(1024).decode()
                if not msg:
                    raise ConnectionResetError

                if msg.strip() == f"{name}:bye":
                    self.broadcast_message(name, f"{name} has left the chat!")
                    Server.Clients.remove(client)
                    sock.close()
                    break

                elif msg.startswith("!who"):
                    client_list = ", ".join([c['client_name'] for c in Server.Clients])
                    sock.send(f"!who: {client_list}".encode())

                elif msg.startswith("!connect"):
                    _, target_name = msg.split(" ")
                    target = self.find_client_by_name(target_name)
                    if target:
                        client['connected_client'] = target_name
                        target['connected_client'] = name

                        ip, port = target['udp_address']
                        sock.send(f"!connect:{target_name}:{ip}:{port}".encode())

                        tip, tport = client['udp_address']
                        target['client_socket'].send(f"!connect:{name}:{tip}:{tport}".encode())
                    else:
                        sock.send("User not found.".encode())

                elif msg == "!disconnect":
                    if client['connected_client']:
                        target = self.find_client_by_name(client['connected_client'])
                        if target:
                            target['connected_client'] = None
                            target['client_socket'].send("!disconnect".encode())
                        client['connected_client'] = None
                        sock.send("!disconnect".encode())

                else:
                    self.broadcast_message(name, msg)

            except:
                self.broadcast_message(name, f"{name} has left the chat!")
                if client in Server.Clients:
                    Server.Clients.remove(client)
                sock.close()
                break

    def find_client_by_name(self, name):
        for c in self.Clients:
            if c['client_name'].lower() == name.lower():
                return c
        return None

    def broadcast_message(self, sender, msg):
        for c in self.Clients:
            if c['client_name'] != sender:
                c['client_socket'].send(msg.encode())

if __name__ == '__main__':
    Server('127.0.0.1', 7632).listen()