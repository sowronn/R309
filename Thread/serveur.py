import socket
import threading

state = True
clients = []  # List to store client connections
blacklist = set("192.168.1.3")  # Use a set for faster lookup

def is_ip_allowed(client_address):
    """
    Check if the IP address is allowed based on the blacklist.

    Parameters:
    - client_address (tuple): The IP address of the client.

    Returns:
    - bool: True if the IP address is allowed, False otherwise.
    """
    return client_address[0] not in blacklist

def broadcast(message, sender_conn):
    """
    Send a message to all clients, including the sender.

    Parameters:
    - message (str): The message to be broadcasted.
    - sender_conn (socket): The connection of the sender.
    """
    for client_conn, username in clients.copy():
        try:
            # Send the message to all clients, including the sender
            client_conn.send((f"{message}" + '\n').encode())
        except Exception as e:
            print(f"Error sending message to client: {e}")

def send_chat_log(conn):
    """
    Send the chat log to a new client.

    Parameters:
    - conn (socket): The connection of the new client.
    """
    try:
        with open("chat_log.txt", "r") as file:
            chat_log = file.read()
            conn.send(chat_log.encode())
    except FileNotFoundError:
        pass  # The file doesn't exist yet, no problem

def save_message(message):
    """
    Save a message to the chat log file.

    Parameters:
    - message (str): The message to be saved.
    """
    with open("chat_log.txt", "a") as file:
        file.write(message + "\n")

def handle_client(conn, address):
    """
    Handle communication with a client.

    Parameters:
    - conn (socket): The connection of the client.
    - address (tuple): The IP address and port of the client.
    """
    global state

    try:
        username = conn.recv(1024).decode()
        clients.append((conn, username))

        if not is_ip_allowed(address):
            print(f"Connection denied for IP address {address[0]} (in the blacklist).")
            conn.close()
            return

        broadcast(f"{username} has joined the discussion!", conn)

        # Send the list of previous messages to the new client
        send_chat_log(conn)

        while state:
            message = conn.recv(1024).decode()

            if not message:
                break

            if message.lower() == 'stop':
                print("Server shutdown")
                state = False
                break
            elif message.lower() == 'bye':
                print(f'Client {username} disconnected...')
                break
            else:
                # Save the message to the file
                save_message(f"{username}: {message}")

                # Send the message to all clients, including the sender
                broadcast(f"{username}: {message}", conn)
    except Exception as e:
        print(f"Communication error with client {address}: {e}")

    clients.remove((conn, username))
    conn.close()
    print(f"Connection closed for {address}")

def main():
    """
    Main function for the server.
    """
    global state
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1024))
    server_socket.listen(10)

    print('Waiting for connections...')

    while state:
        conn, address = server_socket.accept()
        print(f'Client connected {address}')

        threading.Thread(target=handle_client, args=(conn, address), daemon=True).start()

if __name__ == "__main__":
    main()
