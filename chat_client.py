import socket
import os
from threading import Thread

class Client:
    def __init__(self, HOST, PORT):
        self.name = input("Enter your name: ")
        self.tcp_socket = socket.socket()
        self.tcp_socket.connect((HOST, PORT))

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(('', 0))
        self.udp_port = self.udp_socket.getsockname()[1]

        self.tcp_socket.send(f"{self.name}|{self.udp_port}".encode())

        self.connected_client = None
        self.connected_udp_addr = None
        self.clients = []

        print("Digit !help to view available commands.")
        Thread(target=self.receive_tcp_messages).start()
        Thread(target=self.receive_udp_messages).start()
        self.handle_commands()

    def handle_commands(self):
        while True:
            user_input = input("")
            if user_input.startswith("!"):
                self.process_command(user_input)
            else:
                if self.connected_udp_addr:
                    msg = f"{self.name}: {user_input}"
                    self.udp_socket.sendto(msg.encode(), self.connected_udp_addr)
                else:
                    self.tcp_socket.send(f"{self.name}: {user_input}".encode())

    def process_command(self, cmd):
        if cmd == "!help":
            print("Available commands: \n"
                  "!help - Show available commands \n"
                  "!quit - Terminate the connection \n"
                  "!who - List connected users !connect <name> - Start a private chat with a user \n"
                  "!disconnect - Disconnect from the current private chat")

        elif cmd == "!quit":
            self.tcp_socket.send(f"{self.name}:bye".encode())
            os._exit(0)

        elif cmd == "!who":
            self.tcp_socket.send("!who".encode())

        elif cmd.startswith("!connect "):
            self.tcp_socket.send(cmd.encode())

        elif cmd == "!disconnect":
            self.tcp_socket.send("!disconnect".encode())
            self.connected_client = None
            self.connected_udp_addr = None

    def receive_tcp_messages(self):
        while True:
            try:
                msg = self.tcp_socket.recv(1024).decode()
                if not msg:
                    os._exit(0)

                if msg.startswith("!who"):
                    self.clients = msg.split(":")[1].split(",")
                    print("Connected users:", [c.strip() for c in self.clients])

                elif msg.startswith("!connect:"):
                    _, peer_name, peer_ip, peer_port = msg.split(":")
                    self.connected_client = peer_name
                    self.connected_udp_addr = (peer_ip, int(peer_port))
                    print(f"Started private chat with {peer_name} via UDP ({peer_ip}:{peer_port})")

                elif msg.startswith("!disconnect"):
                    self.connected_client = None
                    self.connected_udp_addr = None
                    print("Disconnected from private chat.")

                else:
                    print(msg)

            except ConnectionResetError:
                print("Connection to server lost.")
                os._exit(0)

    def receive_udp_messages(self):
        while True:
            try:
                msg, addr = self.udp_socket.recvfrom(1024)
                print(f"[PRIVATE] {msg.decode()}")
            except:
                continue

if __name__ == '__main__':
    Client('127.0.0.1', 7632)
