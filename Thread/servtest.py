import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout

# Server information
host = "127.0.0.1"  # Change this to your server's IP address if necessary
port = 1024

# Initialize global variables
state = True
textArea = None

# Function to handle client communication
def handle_client(conn):
    global state, textArea
    while state:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break
            print(message)

            # Display message in text area
            textArea.append(message)

            # Check for special messages
            if message.lower() == "stop":
                print("Server shutdown")
                state = False
                break
            elif message.lower() == "bye":
                print('Customer disconnected...')
                break

            # Send response to client
            conn.send((f"Server message: {textArea.toPlainText()}").encode())
        except Exception as e:
            print(f"Communication error with customer : {e}")
            break

    conn.close()

# Function to connect to the server
def connect():
    global state
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send("CONNECT".encode())
            response = s.recv(1024).decode()
            if response == "CONNECTED":
                print("Connected to server")
            else:
                print("Error connecting to server")
    except Exception as e:
        print(e)

# Function to send message to server
def sendToServer(message):
    global textArea
    server_message = f"Server message: {message}"
    textArea.append(server_message)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send(server_message.encode())
    except Exception as e:
        print(f"Error sending message to server: {e}")

# Main function
def main():
    global state, textArea

    # Create GUI application and window
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("Server GUI")

    # Create text area and line edit for user input
    textArea = QTextEdit(window)
    textArea.setReadOnly(True)
    textArea.setFixedHeight(200)

    lineEdit = QLineEdit(window)
    lineEdit.setFixedHeight(50)

    # Create button to send messages to server
    sendButton = QPushButton("Send", window)
    sendButton.clicked.connect(lambda: sendToServer(lineEdit.text()))

    # Layout the widgets
    layout = QVBoxLayout()
    layout.addWidget(textArea)
    layout.addWidget(lineEdit)
    layout.addWidget(sendButton)

    window.setLayout(layout)
    window.show()

    # Connect to the server
    connect()


if __name__ == "__main__":
    main()
