#-*- coding:utf-8 -*-
import socket 
import threading 
import tkinter as tk
from tkinter import *

class ChatClient:
    svrIP = '127.0.0.1'
    port = 2500
    name = ''
    
    def conn(self):
        self.client_sock = socket.socket() # TCP Socket (socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect((ChatClient.svrIP, ChatClient.port)) # Try to connect server 
        print('Connected to ', ChatClient.svrIP, ChatClient.port) 
        self.allChat = ''

    def ui(self): # UI setup
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
        self.chatinput.bind('<Return>', self.send)
        self.sendBtn.bind('<ButtonRelease-1>',self.send)

    def userName(self):
        self.popup = tk.Tk()
        self.popup.wm_title("Set User Name")
        self.label_name = tk.Label(self.popup, text="사용할 이름을 입력해주세요")
        self.label_name.pack(side="top", fill="x", pady=10)
        self.input_name = tk.Entry(self.popup, width = 10)
        self.input_name.pack(fill="x")
        self.okBtn = tk.Button(self.popup, text="입장")
        
        self.okBtn.pack()
        self.input_name.bind('<Return>', self.setUserName)
        self.okBtn.bind('<ButtonRelease-1>',self.setUserName)
        self.popup.mainloop()
    
    def setUserName(self,e): 
        send_data = self.input_name.get()
        self.input_name.delete(0, tk.END)
        self.input_name.config(text='')
        print(type(send_data))
        send_data = send_data.encode(encoding='utf-8')
        print(self.client_sock)
        self.client_sock.sendall(send_data)
        print('전송')
        self.popup.destroy()

    def send(self,e): 
        send_data = self.chatinput.get()
        self.chatinput.delete(0, tk.END)
        self.chatinput.config(text='')
        print(type(send_data))
        send_data = send_data.encode(encoding='utf-8')
        print(self.client_sock)
        self.client_sock.sendall(send_data)
        print('전송')


    def recv(self): 
        while True: 
            recv_data = self.client_sock.recv(1024).decode() + '\n' 
            print(recv_data) 
            self.allChat += recv_data
            print(self.allChat)
            self.contents.config(text=self.allChat)

    def run(self):
        self.conn()
        self.userName()
        self.ui()

        thread = threading.Thread(target=self.recv)
        thread.start()

        self.ui.mainloop()

def main():
    cc = ChatClient()
    cc.run()


main()




    
   