#-*- coding:utf-8 -*-
import socket
import threading

class Room: 
    def __init__(self):
        self.clients = []
        self.allChat=None

    def addClient(self, c):  # add Client
        self.clients.append(c)

    def delClient(self, c): # delete Client
        self.clients.remove(c)

    def sendMsgAll(self, msg):  # send msg to all
        for i in self.clients:
            i.Send(msg)


class ChatClient:  
    def __init__(self, r, soc):
        self.room = r  
        self.id = None  # Client id
        self.soc = soc  

    def Recv(self):
        self.id = self.soc.recv(1024).decode()
        msg = self.id + '님이 입장하셨습니다'
        self.room.sendMsgAll(msg)

        while True:
            msg = self.soc.recv(1024).decode()  # read msg
            if msg == '/종료':  
                self.soc.sendall(msg.encode(encoding='utf-8'))  # send exit msg to sender
                self.room.delClient(self)
                break
            msg = self.id+': '+ msg
            self.room.sendMsgAll(msg)  # send msg to all
        self.room.sendMsgAll(self.id + '님이 퇴장하셨습니다.')

    def Send(self, msg):
        self.soc.sendall(msg.encode(encoding='utf-8'))


class ChatServer:
    svrIP = '127.0.0.1'  # default
    port = 2500

    def __init__(self):
        self.server_soc = None
        self.room = Room()

    def open(self):
        self.server_soc = socket.socket() # TCP socket (socket.AF_INET, socket.SOCK_STREAM)
        self.server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_soc.bind((ChatServer.svrIP, ChatServer.port))
        self.server_soc.listen()

    def run(self):
        self.open()
        print('Server Opened')

        while True:
            client_soc, addr = self.server_soc.accept()
            print(addr, 'Connected')
            c = ChatClient(self.room, client_soc)
            self.room.addClient(c)
            th = threading.Thread(target=c.Recv)
            th.start()

        self.server_soc.close()


def main():
    cs = ChatServer()
    cs.run()


main()