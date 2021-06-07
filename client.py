#-*- coding:utf-8 -*-
import socket 
import threading 
import tkinter as tk
from tkinter import *

class ChatClient:
    svrIP = '127.0.0.1'
    port = 2500
    
    def conn(self):
        # Connection
        self.client_sock = socket.socket() # TCP Socket (socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect((ChatClient.svrIP, ChatClient.port)) # 서버로 연결시도 
        print('Connected to ', ChatClient.svrIP, ChatClient.port) 
        self.allChat = ''

    def ui(self):
        # GUI
        self.ui = tk.Tk()
        self.ui.title('201744021 송휘 TCP/IP')
        self.ui.geometry('400x490')
        self.ui.resizable(False, False)

        self.contents = tk.Label(self.ui, justify = "left")
        self.chatinput = tk.Entry(self.ui, width = 40)
        self.sendBtn = tk.Button(self.ui,width = 10, text = '전송')

        self.contents.place(x=10, y=10)
        self.chatinput.place(x = 10, y = 450)
        self.sendBtn.place(x = 300, y = 446)
        self.chatinput.bind('<Return>', self.Send)
        self.sendBtn.bind('<ButtonRelease-1>',self.Send)

       
    def Send(self,e): 
        send_data = self.chatinput.get()
        self.chatinput.delete(0, tk.END)
        self.chatinput.config(text='')
        print(type(send_data))
        send_data = send_data.encode(encoding='utf-8')
        print(self.client_sock)
        self.client_sock.sendall(send_data)
        print('전송')


    def Recv(self): 
        while True: 
            recv_data = self.client_sock.recv(1024).decode() + '\n' 
            print(recv_data) 
            self.allChat += recv_data
            print(self.allChat)
            self.contents.config(text=self.allChat)

    def run(self):
        self.conn()
        self.ui()

        th2 = threading.Thread(target=self.Recv)
        th2.start()

        self.ui.mainloop()

def main():
    cc = ChatClient()
    cc.run()


main()




    
   