from sys import exit
import socket
import time
from threading import *
from _thread import *

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        print("connected")
        self.sock = socket
        self.addr = address
        self.text = ""
        self.command = ""
        self.args = []
        self.start()

    def reset(self):
        self.command = ""
        self.args = []
        self.text = ""

    def run(self):
        while True:
            if self.text != "":
                print("writing text")
                self.sock.send((self.text + '\n').encode())
                self.text = ""

                print("reading messages")
                command, *args = self.sock.recv(1024).decode('ascii').split(' ')
                self.command = command
                self.args = args

                print(command)
                time.sleep(1)





class Server(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # self.host = '192.168.0.3'
        self.host = '10.200.33.219'
        self.port = 6980

        self.ss.bind((self.host, self.port))
        self.ss.listen(5)
        self.clients = []
        self.start()

    def run(self):
        while 1:
            clientsocket, address = self.ss.accept()
            self.clients.append(client(clientsocket, address))
