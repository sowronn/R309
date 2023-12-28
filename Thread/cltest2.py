import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QPushButton, QVBoxLayout

clt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clt_socket.connect(("127.0.0.1", 1024))


class GUI(QWidget):

    def __init__(self):
        super().__init__()

        self.textArea = QTextEdit()
        self.textArea.setReadOnly(True)
        self.textArea.setFixedHeight(200)

        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedHeight(50)

        # Create the send button
        self.sendButton = QPushButton("Send", self)
        self.sendButton.setFixedHeight(50)

        # Connect the button to the sendMessage() method
        self.sendButton.clicked.connect(self.sendMessage)

        layout = QVBoxLayout()
        layout.addWidget(self.textArea)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.sendButton)

        self.setLayout(layout)

        # Show the window
        self.show()

    def sendMessage(self):
        # Get the message from the line edit
        message = self.lineEdit.text()

        # Send the message to the server
        clt_socket.send(message.encode())

        # Clear the line edit
        self.lineEdit.clear()


class Client(threading.Thread):

    def __init__(self):
        super().__init__(daemon=True)

    def receiveMessage(self):
        while True:
            # Receive a message from the server
            try:
                message = clt_socket.recv(1024).decode()
                # Insert the message to the GUI
                self.window.textArea.insertPlainText(message)
            except Exception as e:
                # An error occurred, stop the thread
                print(f"Communication error with server : {e}")
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    client.start()
    window = GUI()
    window.show()

    sys.exit(app.exec_())