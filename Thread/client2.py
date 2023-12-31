import socket
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QInputDialog
from PyQt5.QtCore import QObject, pyqtSignal, QThread


class ClientThread(QObject):
    message_received = pyqtSignal(str)

    def run(self):
        """
        Continuously receive messages from the server.

        Emits the received message to update the GUI.

        Raises:
        - Exception: If an error occurs during message reception.
        """
        while True:
            try:
                message = clt_socket.recv(1024).decode()
                self.message_received.emit(message)
            except Exception as e:
                print(f"Error during message reception: {e}")
                break


class GUI(QWidget):
    def __init__(self):
        """
        Initialize the GUI window.

        Sets up the user interface with a text area, input field, and send button.
        Creates a thread for receiving messages from the server.

        Raises:
        - Exception: If an error occurs during GUI initialization.
        """
        super().__init__()

        self.username, okPressed = QInputDialog.getText(self, "Username", "Enter your username:",
                                                        QLineEdit.Normal, "")
        if okPressed and self.username:
            # Send the username to the server upon the first request
            clt_socket.send(self.username.encode())

        self.textArea = QTextEdit()
        self.textArea.setReadOnly(True)
        self.textArea.setFixedHeight(200)

        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedHeight(50)

        self.sendButton = QPushButton("Send", self)
        self.sendButton.setFixedHeight(50)
        self.sendButton.clicked.connect(self.sendMessage)

        layout = QVBoxLayout()
        layout.addWidget(self.textArea)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.sendButton)
        self.setLayout(layout)

        # Show the window
        self.show()

        # Create a thread for receiving messages
        self.client_thread = ClientThread()
        self.client_thread.message_received.connect(self.updateTextArea)
        self.client_thread_thread = QThread()
        self.client_thread.moveToThread(self.client_thread_thread)
        self.client_thread_thread.started.connect(self.client_thread.run)
        self.client_thread_thread.start()

    def init_connection(self):
        """
        Initialize the connection to the server.

        Establishes a socket connection and sends the client's IP address for verification.

        Raises:
        - Exception: If an error occurs during the connection initialization.
        """
        global clt_socket, client_ip
        client_ip = "192.168.1.2"  # Replace this with your actual implementation
        clt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clt_socket.connect(("127.0.0.1", 1024))

        # Send the IP address to the server for verification
        clt_socket.send(client_ip.encode())

    def sendMessage(self):
        """
        Send a message to the server.

        Retrieves the message from the input field, sends it to the server, and clears the input field.
        """
        message = self.lineEdit.text()
        clt_socket.send(message.encode())
        self.lineEdit.clear()

    def updateTextArea(self, message):
        """
        Update the text area with a received message.

        Parameters:
        - message (str): The message received from the server.
        """
        self.textArea.insertPlainText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    clt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clt_socket.connect(("127.0.0.1", 1024))

    window = GUI()
    sys.exit(app.exec_())
