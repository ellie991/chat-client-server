# Python Chat Client-Server

A simple **client-server chat application** built in Python using sockets and multithreading.  
The project supports:

- **TCP** connection for broadcast messaging
- **UDP** peer-to-peer connection for private messages

It allows multiple clients to connect to a server and exchange messages in real time via the terminal.

---

## Features

- Start a **server** to manage up to **5 simultaneous clients**
- Real-time **broadcast messaging** to all connected users (via TCP)
- **Private messaging** between two users (via UDP)
- Simple terminal interface for sending/receiving messages
- Manual setup of client identity and ports

## Technologies

- Python 3
- `socket` module (standard library)
- `threading` module for concurrent client handling

## How to Run

### 1. Start the server
- 127.0.0.1 = local loopback address
- 8888 = TCP port the server will listen on

```bash
python chat_server.py 127.0.0.1 8888
```

### 2. Start clients
Choose your names, loopback address and id port. 
- A name
- 127.0.0.1 = local loopback address, server IP
- unique port fot the client
  
Examples:
```bash
python chat_client.py Alice 127.0.0.1 2000
```
```bash
python chat_client.py Bob 127.0.0.1 2001
```
```bash
python chat_client.py Tom 127.0.0.1 2002
```
