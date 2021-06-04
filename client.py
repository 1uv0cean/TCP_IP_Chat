#-*- coding:utf-8 -*-
import socket 
import threading 
import tkinter
from tkinter import *

def Send(client_sock): 
    while True: 
        send_data = bytes(input().encode()) # 사용자 입력 
        client_sock.send(send_data) # Client -> Server 데이터 송신 

def Recv(client_sock): 
    while True: 
        recv_data = client_sock.recv(1024).decode() # Server -> Client 데이터 수신 
        print(recv_data) 
        
#TCP Client 
if __name__ == '__main__': 
    Ui.title = "송휘"
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP Socket 
    svrIP = input(("Server IP(defalut: 127.0.0.1): ")) #통신할 대상의 IP 주소 
    if svrIP == '':
        svrIP = '127.0.0.1'
    port = input(("port(defalut: 2500): ")) #통신할 대상의 port 주소 
    if port == '':
        port = 2500
    else:
        port = int(port)
    client_sock.connect((svrIP, port)) #서버로 연결시도 
    print('Connected to ', svrIP, port) 

    #Client의 메시지를 보낼 쓰레드 
    thread1 = threading.Thread(target=Send, args=(client_sock, )) 
    thread1.start() 

    #Server로 부터 다른 클라이언트의 메시지를 받을 쓰레드 
    thread2 = threading.Thread(target=Recv, args=(client_sock, )) 
    thread2.start()

