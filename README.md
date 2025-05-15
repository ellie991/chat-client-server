# Python Chat Client-Server

A simple **client-server chat application** built with Python using sockets and multithreading. This project allows multiple clients to connect to a server and exchange messages in real time via the terminal.

## Features

- Start a **server** that listens for incoming client connections
- Connect one or more **clients** to the server (max 5)
- Broadcast messages to all connected clients
- Private messages between two users
- Real-time messaging from the terminal
- Basic handling of disconnected clients

## Technologies

- Python 3
- `socket` module (standard library)
- `threading` module for concurrent client handling

## How to Run

### 1. Start the server

```bash
python chat_server.py 127.0.0.1 8888
```

### 2. Start clients
examples
```bash
python chat_client.py Alice 127.0.0.1 2000
```
```bash
python chat_client.py Bob 127.0.0.1 2001
```
