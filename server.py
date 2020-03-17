import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork

def Run_Server():
    app = QtCore.QCoreApplication(sys.argv)
    SOCKET = QtNetwork.QUdpSocket()

    def Bind_Server(HOST = "127.0.0.1", PORT = 33002):
        SOCKET.bind(QtNetwork.QHostAddress(HOST), PORT)

    def Send_Message(message, client, port):
        SOCKET.writeDatagram(message.encode(), QtNetwork.QHostAddress(client), port)

    def Receive_Message():
        while SOCKET.hasPendingDatagrams():
            received_message, received_client, received_port = SOCKET.readDatagram(SOCKET.pendingDatagramSize())
            received_message = received_message.decode()
            received_client = received_client.toString()

            if received_message.startswith("{CONNECT}"):
                print(f"{received_client}:{str(received_port)} has connected.")

            if received_message.startswith("{DISCONNECT}"):
                SOCKET.close()
                break

            if received_message.startswith("{REGISTER}"):
                new_message = f"{{MSG}}Welcome {received_client}!"
                Send_Message(new_message, received_client, received_port)

            if received_message.startswith("{UNREGISTER}"):
                new_message = f"{{MSG}}Bye {received_client}!"
                Send_Message(new_message, received_client, received_port)

            if received_message.startswith("{ALL}"):
                new_message = f"{{MSG}} {received_message}"
                Send_Message(new_message, received_client, received_port)

    Bind_Server()
    SOCKET.readyRead.connect(Receive_Message)
    sys.exit(app.exec_())

if __name__ == "__main__":
    Run_Server()