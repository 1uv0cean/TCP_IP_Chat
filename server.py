#-*- coding:utf-8 -*-
from tkinter import *
from threading import *
import socket


global client_1, client_2
client_1 = ''
client_2 = ''
name1 =  ''
name2 =  ''

IP = "127.0.0.01" # default IP
PORT = "2500" # default Port

class createServer:
    def __init__(self, UI):
        self.ui = UI
        UI.title("201744021 송휘 - Server")
        UI.geometry("200x100")
        self.mainFrame = Frame(self.ui)
        self.mainFrame.pack(fill = X)

        self.subFrame = Frame(self.ui)
        self.subFrame.pack(fill = X)
        self.subFrame1 = Frame(self.ui)
        self.subFrame1.pack(fill = X)
        self.subFrame2 = Frame(self.ui)
        self.subFrame2.pack(fill = X)
        self.subFrame3 = Frame(self.ui)
        self.subFrame3.pack(fill = X)

        self.label = Label(self.subFrame, text = "채팅방 생성")
        self.label.pack(side = TOP)


        self.emptylabel1 = Label(self.subFrame1, text = "   ")
        self.emptylabel1.pack(side = LEFT)
        self.label1 = Label(self.subFrame1, text = "IP                           ")
        self.label1.pack(side = LEFT)
        self.label2 = Label(self.subFrame1, text = "PORT")
        self.label2.pack(side = LEFT)

        self.emptylabel2 = Label(self.subFrame2, text = "   ")
        self.emptylabel2.pack(side = LEFT)
        self.entry1 = Entry(self.subFrame2, width = 15)
        self.entry1.pack(side = LEFT)
        self.emptylabel3 = Label(self.subFrame2, text = "   ")
        self.emptylabel3.pack(side = LEFT)
        self.entry2 = Entry(self.subFrame2, width = 5)
        self.entry2.pack(side = LEFT)
        self.button = Button(self.subFrame3, text = "연결", width = 10, height = 2, command = self.openserver)
        self.button.pack(side = TOP)

    def openserver(self):
        global IP, PORT
        IP = self.entry1.get()
        PORT = int(self.entry2.get())
        self.ui.quit()
        self.ui.destroy()

root = Tk()
app = createServer(root) 
root.mainloop()
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((IP,PORT))
server_sock.listen(2)
count = 0
connection = 0

def socket1():
    
    count += 1
    client1, addr1 = server_sock.accept()
    print("[알림] :{0} 연결".format(str(addr1[1])))
    connection+=1
    name1 = client1.recv(65535)
    sendmessage("[System] {0}님이 입장하셨습니다.".format(name1))
    while True:
        data1 = client1.recv(65535)
