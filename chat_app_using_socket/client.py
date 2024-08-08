import socket
import tkinter as tk
import threading

# Initialize the main window
window = tk.Tk()
window.geometry("500x400+500+100")
window.title("MESSENGER")

# Layout configuration
window.columnconfigure([1, 2, 3, 4], weight=1)
holder_client_index = ""

# Socket functions
def send_message():
    try:
        message = message_textbox.get()
        message_textbox.delete(0, tk.END)
        chat_box.insert(tk.END, f"Client #{holder_client_index}: {message}\n")
        client_socket.send(message.encode())
    except Exception as e:
        print(f"Error sending message: {e}")

def handle_messages(client_socket):
    while True:
        try:
            incoming_message = client_socket.recv(2000).decode()
            if not incoming_message:
                break
            message_parts = incoming_message.split(":")
            if len(message_parts) == 2:
                client_index, message = message_parts
                chat_box.insert(tk.END, f"Client #{client_index}: {message}\n")
                chat_box.update_idletasks()
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def update_client_index(new_client_index):
    global holder_client_index
    holder_client_index = int(new_client_index)
    client_box.delete(1.0, tk.END)
    for index in range(1, holder_client_index + 1):
        client_box.insert(tk.END, f"Client #{index}\n")
        client_box.update_idletasks()

# GUI Elements
chat_box = tk.Text(background="white", border=5, width=40, height=20)
chat_box.grid(row=1, column=2, columnspan=1)

client_box = tk.Text(background="white", border=5, width=20, height=20)
client_box.grid(row=1, column=4)

send_label = tk.Label(text="SEND:", font=("Arial", 10), width=4)
send_label.grid(row=2, column=1, padx=0, pady=0)

message_textbox = tk.Entry(width=50)
message_textbox.grid(row=2, column=2, columnspan=2)

send_button = tk.Button(text=">", font=("Arial", 10), height=0, command=send_message)
send_button.grid(row=2, column=3, columnspan=2, ipadx=40)

# Socket connection
def get_ip_address():
    try:
        ip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_socket.connect(('8.8.8.8', 80))
        ip_address = ip_socket.getsockname()[0]
        ip_socket.close()
        return ip_address
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return "127.0.0.1"

server_ip_address = ""  # ENTER SERVER IP ADDRESS
port_address = 12345
ip_address = get_ip_address()

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip_address, port_address))
    print("Connected to Server:", server_ip_address)
except Exception as e:
    print(f"Error connecting to server: {e}")

def receive_client_index():
    while True:
        try:
            client_index = client_socket.recv(2000).decode()
            if not client_index:
                break
            client_index_parts = client_index.split()
            if len(client_index_parts) >= 2:
                client_index = client_index_parts[1][1:]
                global holder_client_index
                holder_client_index = int(client_index)
                update_client_index(holder_client_index)
        except Exception as e:
            print(f"Error receiving client index: {e}")
            break

update_client_index_newthread = threading.Thread(target=receive_client_index)
update_client_index_newthread.start()

handle_message_newthread = threading.Thread(target=handle_messages, args=(client_socket,))
handle_message_newthread.start()

# Start the Tkinter main loop
window.mainloop()
