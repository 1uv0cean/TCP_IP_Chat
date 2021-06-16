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
        self.ui.geometry('515x330')
        self.ui.resizable(False, False)
        
        self.contentsFrame = Frame(self.ui)
        self.clientsFrame = Frame(self.ui)
        self.scrollbar = Scrollbar(self.contentsFrame)
        self.scrollbar.pack(side='right',fill='y')
        self.scrollbar2 = Scrollbar(self.clientsFrame)
        self.scrollbar2.pack(side='right',fill='y')
        self.contents = Text(self.contentsFrame, width = 52, height = 21 ,yscrollcommand = self.scrollbar.set)
        self.contents.pack(side='left')
        self.clients = Text(self.clientsFrame, width = 12, height = 20,yscrollcommand = self.scrollbar2.set)
        self.clients.pack(side='left')
        self.chatinput = tk.Entry(self.ui, width = 43)
        self.sendBtn = tk.Button(self.ui,width = 10, text = '전송')
        self.label = tk.Label(text="참여자")

        self.scrollbar['command'] = self.contents.yview
        self.scrollbar2['command'] = self.clients.yview
        self.contentsFrame.place(x=10, y=10)
        self.label.place(x=425)
        self.clientsFrame.place(x=405, y=22)
        self.chatinput.place(x = 10, y = 300)
        self.sendBtn.place(x = 320, y = 297)
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
        self.send_data = self.input_name.get()
        self.input_name.delete(0, tk.END)
        self.input_name.config(text='')
        self.send_data = self.send_data.encode(encoding='utf-8')
        self.client_sock.sendall(self.send_data)
        self.popup.destroy()
        

    def send(self,e): 
        send_data = self.chatinput.get()
        self.chatinput.delete(0, tk.END)
        self.chatinput.config(text='')
        send_data = send_data.encode(encoding='utf-8')
        self.client_sock.sendall(send_data)


    def recv(self): 
        while True:
            recv_data = self.client_sock.recv(1024).decode() + '\n'
            print(recv_data)
            while True:
                if recv_data[0:6] == "[접속명단]":
                    clientList = str(recv_data).split("|")
                    del clientList[0]
                    welcomMsg=clientList[len(clientList)-1]
                    del clientList[len(clientList)-1]
                    print(clientList)
                    self.clients.delete("1.0", "end")
                    for i in clientList:
                        self.clients.insert("end",i+'\n')
                    self.contents.insert("end",str(welcomMsg))
                    break
                else:         
                    self.allChat += recv_data
                    self.contents.insert("end",str(recv_data))
                    break
                '''
                elif recv_data[0:6] == "[끝말잇기]":
                    shiritori = str(recv_data).split("|")
                    print(shiritori)
                    self.contents.insert("end",shiritori[1]+shiritori[2])
                    lastword = shiritori[2]
                    break
                '''
                
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




    
   