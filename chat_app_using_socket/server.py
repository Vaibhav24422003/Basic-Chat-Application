import socket
import tkinter as tk
import threading
import time

connected_clients = []
host_address = '0.0.0.0'
port_address = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_address, port_address))
server_socket.listen(5)
print("Server: Listening for incoming connections...")

def handle_client(client_socket, client_address):
    while True: 
        message = client_socket.recv(2000).decode()
        holder_client_index = connected_clients.index(client_socket) + 1
        if not message:
            break
        print(f"Client #{holder_client_index}, SENT: {message}")

        for client in connected_clients:
            if client != client_socket:
                    client.send(f"{holder_client_index}:{message}".encode())
    
def update_client_index():
    for index, client in enumerate(connected_clients):
        client_index = index + 1
        client.send(str(client_index).encode())

def connection_manager():
    initial_connection_number = len(connected_clients)
    while True: 
        client_socket, client_address = server_socket.accept()
        print("Server: Connected to Client: ", client_address)
        connected_clients.append(client_socket)
        client_index = connected_clients.index(client_socket) + 1
        
        if len(connected_clients) > initial_connection_number:
            for client in connected_clients:
                announce_login = f"Client #{client_index} joined!\n"
                client.send(announce_login.encode())
            update_index_newthread = threading.Thread(target=update_client_index)
            update_index_newthread.start()
            
                
        client_newthread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_newthread.start()



connection_manager_newthread = threading.Thread(target=connection_manager)
connection_manager_newthread.start()