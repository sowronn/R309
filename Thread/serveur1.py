import socket
import threading

state = True

def handle_client(conn):
    global state
    while state:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break
            print(message)

            if message.lower() == 'stop':
                print("server shutdown")
                state = False
                break
            elif message.lower() == 'bye':
                print('Customer disconnected...')
                break
        except Exception as e:
            print(f"Communication error with customer : {e}")
            break

    conn.close()

def main():
    global state
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1024))
    server_socket.listen(10)

    print('waiting for connection...')

    while state:
        conn, address = server_socket.accept()
        print(f'Customer connected {address}')
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    main()
