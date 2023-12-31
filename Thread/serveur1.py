import socket
import threading

state = True
clients = []  # Liste pour stocker les connexions des clients
blacklist = set("192.168.1.3")  # Utilisez un ensemble pour une recherche plus rapide

def is_ip_allowed(client_address):
    """Vérifie si l'adresse IP n'est pas dans la blacklist."""
    return client_address[0] not in blacklist

def broadcast(message, sender_conn):
    for client_conn, username in clients.copy():
        try:
            # Envoyer le message à tous les clients, y compris l'émetteur
            client_conn.send((f"{message}" + '\n').encode())
        except Exception as e:
            print(f"Erreur lors de l'envoi du message au client : {e}")

def send_chat_log(conn):
    try:
        with open("chat_log.txt", "r") as file:
            chat_log = file.read()
            conn.send(chat_log.encode())
    except FileNotFoundError:
        pass  # Le fichier n'existe pas encore, pas de problème

def save_message(message):
    with open("chat_log.txt", "a") as file:
        file.write(message + "\n")

def handle_client(conn, address):
    global state

    try:
        username = conn.recv(1024).decode()
        clients.append((conn, username))

        if not is_ip_allowed(address):
            print(f"Connexion refusée pour l'adresse IP {address[0]} (dans la blacklist).")
            conn.close()
            return

        broadcast(f"{username} a rejoint la discussion!", conn)

        # Envoyer la liste des messages précédents au nouveau client
        send_chat_log(conn)

        while state:
            message = conn.recv(1024).decode()

            if not message:
                break

            if message.lower() == 'stop':
                print("Arrêt du serveur")
                state = False
                break
            elif message.lower() == 'bye':
                print(f'Client {username} déconnecté...')
                break
            else:
                # Enregistrer le message dans le fichier
                save_message(f"{username}: {message}")

                # Envoyer le message à tous les clients, y compris l'émetteur
                broadcast(f"{username}: {message}", conn)
    except Exception as e:
        print(f"Erreur de communication avec le client {address}: {e}")

    clients.remove((conn, username))
    conn.close()
    print(f"Connection closed for {address}")

def main():
    global state
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1024))
    server_socket.listen(10)

    print('En attente de connexion...')

    while state:
        conn, address = server_socket.accept()
        print(f'Client connecté {address}')

        threading.Thread(target=handle_client, args=(conn, address), daemon=True).start()

if __name__ == "__main__":
    main()
