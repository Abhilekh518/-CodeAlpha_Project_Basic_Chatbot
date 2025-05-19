import socket
import threading
from datetime import datetime

clients = []
usernames = {}

def broadcast(message, sender_socket, is_binary=False):
    for client in clients:
        if client != sender_socket:
            try:
                if is_binary:
                    client.send(message)
                else:
                    client.send(message.encode('utf-8'))
            except:
                clients.remove(client)

def handle_client(client_socket):
    try:
        # Receive username first
        username = client_socket.recv(1024).decode('utf-8')
        usernames[client_socket] = username
        print(f"{username} joined.")

        while True:
            header = client_socket.recv(1024).decode('utf-8')
            if not header:
                continue

            if header.startswith("FILE:"):
                _, filename, filesize = header.split(":", 2)
                filesize = int(filesize)

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                info_msg = f"[{timestamp}] Incoming file '{filename}' from {username}."
                broadcast(info_msg, client_socket)

                remaining = filesize
                file_data = b""
                while remaining > 0:
                    chunk = client_socket.recv(min(4096, remaining))
                    if not chunk:
                        break
                    file_data += chunk
                    remaining -= len(chunk)

                broadcast(f"FILE:{filename}:{filesize}", client_socket)
                broadcast(file_data, client_socket, is_binary=True)

            elif header.startswith("TYPING:"):
                broadcast(header, client_socket)

            else:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message_with_timestamp = f"[{timestamp}] {header}"
                broadcast(message_with_timestamp, client_socket)

    except Exception as e:
        print(f"Client error: {e}")
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(5)
    print("Server is running...")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    start_server()
