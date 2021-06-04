import threading
import socket
import tkinter as tk
from tkinter import *

class UiChatClient:
    ip = '127.0.0.1'
    port = 2500

    def __init__(self):
        self.conn_soc = None  # 서버와 연결된 소켓
        self.win = None
        self.chatCont = None
        self.myChat = None
        self.sendBtn = None
        self.allChat =''

    def conn(self):
        self.conn_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_soc.connect((UiChatClient.ip, UiChatClient.port))

    def setWindow(self):
        self.win = tk.Tk()
        self.win.title('201744021 송휘 TCP/IP')
        self.win.geometry('400x500')
        welcome ='Connected to {0} {1}'.format(self.ip,self.port)
        self.marginTop = tk.Label(self.win)
        self.chatCont = tk.Label(self.win, width=50, height=29, text=welcome,anchor='nw')
        self.myChat = tk.Entry(self.win, width=40)
        self.sendBtn = tk.Button(self.win, width=10, text='전송')

        self.marginTop.grid(row=0)
        self.chatCont.grid(row=1, column=0, columnspan=2)
        self.myChat.grid(row=2, column=0, padx=10)
        self.sendBtn.grid(row=2, column=1)

        self.myChat.bind('<Return>', self.sendMsg)


    def sendMsg(self, e):  # 키보드 입력 받아 상대방에게 메시지 전송
        msg = self.myChat.get()
        self.myChat.delete(0, tk.END)
        self.myChat.config(text='')
        print(type(msg))
        msg = msg.encode(encoding='utf-8')
        print(self.conn_soc)
        self.conn_soc.sendall(msg)
        print('전송')

    def recvMsg(self):  # 상대방이 보낸 메시지 읽어서 화면에 출력
        while True:
            msg = self.conn_soc.recv(1024)
            print(msg)
            msg = msg.decode()+'\n'
            self.allChat += msg
            print(self.allChat)

            self.chatCont.config(text=self.allChat)
            # if msg == '/stop':
            #     self.close()
            #     break

    def run(self):
        self.conn()
        self.setWindow()

        th2 = threading.Thread(target=self.recvMsg)
        th2.start()
        self.win.mainloop()

    def close(self):
        self.conn_soc.close()
        print('종료되었습니다')


def main():
    conn = UiChatClient()
    conn.run()


main()