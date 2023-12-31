import socket
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QInputDialog
from PyQt5.QtCore import QObject, pyqtSignal, QThread


class ClientThread(QObject):
    message_received = pyqtSignal(str)

    def run(self):
        while True:
            try:
                message = clt_socket.recv(1024).decode()
                self.message_received.emit(message)
            except Exception as e:
                print(f"Erreur lors de la réception du message : {e}")
                break


class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.username, okPressed = QInputDialog.getText(self, "Nom d'utilisateur", "Entrez votre nom d'utilisateur:",
                                                        QLineEdit.Normal, "")
        if okPressed and self.username:
            # Envoyer le nom d'utilisateur au serveur dès la première demande
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

        # Créer le thread pour la réception des messages
        self.client_thread = ClientThread()
        self.client_thread.message_received.connect(self.updateTextArea)
        self.client_thread_thread = QThread()
        self.client_thread.moveToThread(self.client_thread_thread)
        self.client_thread_thread.started.connect(self.client_thread.run)
        self.client_thread_thread.start()

    def init_connection(self):
        global clt_socket, client_ip
        client_ip = "192.168.1.3"  # Remplacez ceci par votre implémentation réelle
        clt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clt_socket.connect(("127.0.0.1", 1024))

        # Envoyer l'adresse IP au serveur pour vérification
        clt_socket.send(client_ip.encode())

    def sendMessage(self):
        message = self.lineEdit.text()
        clt_socket.send(message.encode())
        self.lineEdit.clear()

    def updateTextArea(self, message):
        self.textArea.insertPlainText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    clt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clt_socket.connect(("127.0.0.1", 1024))

    window = GUI()
    sys.exit(app.exec_())

