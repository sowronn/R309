import socket
import threading

state = True
clients = []  # Liste pour stocker les connexions des clients
blacklist = {"192.168.1.2"}
whitelist = {"192.168.1.1"}

def is_ip_allowed(client_address):
    """Vérifie si l'adresse IP est dans la whitelist et pas dans la blacklist."""
    return client_address[0] in whitelist and client_address[0] not in blacklist
def broadcast(message, sender_conn):
    for client_conn in clients:
        try:
            client_conn.send((message + '\n').encode())
        except Exception as e:
            print(f"Erreur lors de l'envoi du message au client : {e}")

def handle_client(conn, client_address):
    global state, username

    # Vérifie si l'adresse IP est autorisée
    if not is_ip_allowed(client_address):
        print(f"Connexion refusée pour l'adresse IP {client_address[0]} (dans la blacklist).")
        conn.close()
        return

    # Ajoute l'adresse IP à la whitelist si elle n'est pas déjà présente
    if client_address[0] not in whitelist:
        whitelist.add(client_address[0])
        print(f"Ajout automatique de l'adresse IP {client_address[0]} à la whitelist.")

    try:
        username = conn.recv(1024).decode()
        clients.append((conn, username))
        broadcast(f"Bienvenue {username}!", conn)

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
                # Diffuse le message à tous les clients, y compris l'émetteur
                broadcast(f"{username}: {message}", conn)
    except Exception as e:
        print(f"Erreur de communication avec le client : {e}")

    # Retire la connexion de la liste des clients actifs
    clients.remove((conn, username))
    conn.close()


def main():
    global state
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1024))
    server_socket.listen(10)

    print('En attente de connexion...')

    while state:
        conn, address = server_socket.accept()
        print(f'Client connecté {address}')

        # Ajoute la connexion à la liste des clients actifs
        clients.append(conn)

        # Lance un thread pour gérer le client
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    main()
