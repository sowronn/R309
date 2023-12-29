import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QInputDialog
from PyQt5.QtCore import QObject, pyqtSignal

client_ip = "192.168.1.3"  # Remplacez ceci par votre implémentation réelle

clt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clt_socket.connect(("127.0.0.1", 1024))
clt_socket.send(client_ip.encode())

class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.username, okPressed = QInputDialog.getText(self, "Nom d'utilisateur", "Entrez votre nom d'utilisateur:",
                                                        QLineEdit.Normal, "")
        if okPressed and self.username:
            # Envoyer le nom d'utilisateur au serveur dès la première demande
            clt_socket.send(self.username.encode())

        elif not okPressed or not self.username:
            print("Nom d'utilisateur invalide. Fermeture de l'application.")
            sys.exit(1)

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

    def sendMessage(self):
        message = self.lineEdit.text()
        clt_socket.send(message.encode())
        self.lineEdit.clear()

    def updateTextArea(self, message):
        self.textArea.insertPlainText(message)


class ClientThreadSignals(QObject):
    message_received = pyqtSignal(str)


class ClientThread(threading.Thread):
    def __init__(self, signals):
        super().__init__(daemon=True)
        self.signals = signals

    def run(self):
        while True:
            try:
                message = clt_socket.recv(1024).decode()
                self.signals.message_received.emit(message)
            except Exception as e:
                print(f"Communication error with server: {e}")
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()

    signals = ClientThreadSignals()
    client_thread = ClientThread(signals)
    client_thread.signals.message_received.connect(window.updateTextArea)
    client_thread.start()

    window.show()
    sys.exit(app.exec_())
