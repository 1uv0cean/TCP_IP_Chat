#-*- coding:utf-8 -*-
import socket
import threading
import re, random


clientsList = []
'''
class game:

    def openDict(self): # open korean dictionary
        with open('dict.txt', 'rt', encoding='utf-8') as self.f:
            self.s = self.f.read()

        self.pat = re.compile('^[ㄱ-ㅎ가-힣]+$')
        self.wordDict = dict()
        self.ivcSet = set()

    def extractWord(self): # korean, word length >= 2
        for i in sorted([i for i in self.s.split() if self.pat.match(i) and len(i) >= 2], key=lambda x:-len(x)):
            if i[0] not in self.wordDict:
                self.wordDict[i[0]] = set()
            self.wordDict[i[0]].add(i)
    
    def deleteWord(self): # delete invincible words 
        for i in self.wordDict:
            self.delList = list()
            for j in self.wordDict[i]:
                if j[-1] not in self.wordDict:
                    self.delList.append(j)
            for j in self.delList:
                self.ivcSet.add(j)
                self.wordDict[i].remove(j)

    def startGame(self): # start game
        game.openDict(self)
        game.extractWord(self)
        game.deleteWord(self)
        
        

        self.lastWord = random.choice(list(self.wordDict[random.choice(list(self.wordDict.keys()))]))
        self.alreadySet = set()
        self.alreadySet.add(self.lastWord)
        
        msg = '[끝말잇기]\n|'+'-' * 50+'\n'
        msg += '게임을 시작합니다.\n시작단어: |'
        msg += self.lastWord
        
        self.room.sendMsgAll(msg)
        
        
        while True:
            
            msg = self.soc.recv(1024).decode()  # read msg
            print(msg)
            firstLetter = msg[0]
            if firstLetter != self.lastWord[-1]:
                msg = " [오류] '" + self.lastWord[-1] + "' (으)로 시작하는 단어를 입력하세요."
            elif msg in self.ivcSet:
                msg = ' [오류] 한방단어는 사용할 수 없습니다.'
            elif msg in self.alreadySet:
                msg = ' [오류] 이미 나온 단어입니다.'
            elif msg not in self.wordDict.get(firstLetter, set()):
                msg = ' [오류] 사전에 없는 단어입니다.'
            else:
                self.alreadySet.add(msg)
                self.lastWord = msg
                msg = self.id+': '+ msg  
            self.room.sendMsgAll(msg)  # send msg to all 
'''

class room: 
    def __init__(self):
        self.clients = []
        self.allChat=None
        
    def addClient(self, c):  # add Client
        self.clients.append(c)

    def delClient(self, c): # delete Client
        self.clients.remove(c)

    def sendMsgAll(self, msg):  # send msg to all
        for i in self.clients:
            i.send(msg)


class chatClient:  
    def __init__(self, r, soc):
        self.room = r  
        self.id = None  # Client id
        self.soc = soc  

    def recv(self):
        self.id = self.soc.recv(1024).decode()
        clientsList.append(self.id)
        self.refreshClient()

        msg = self.id + '님이 입장하셨습니다'
        self.room.sendMsgAll(msg)
        print(msg)

        while True:
            msg = self.soc.recv(1024).decode()  # read msg
            if msg == '/종료':  
                self.soc.sendall(msg.encode(encoding='utf-8'))  # send exit msg to sender
                self.room.delClient(self)
                clientsList.remove(self.id)
                break
            '''
            if msg == '/시작': # shiritori game
                print(self.room.clients)
                self.soc.sendall(game.startGame(self))
                #game.startGame(self)
            '''
            
            msg = self.id+': '+ msg
            self.room.sendMsgAll(msg)  # send msg to all
            print(msg)
        self.room.sendMsgAll(self.id + '님이 퇴장하셨습니다.')
        self.refreshClient()
        
    def refreshClient(self):
        self.sendList = ''
        for i in range(len(clientsList)):
            print(clientsList[i])
            self.sendList += clientsList[i]+"|"
        msg = '[접속명단]|'+ self.sendList
        self.room.sendMsgAll(msg)

    def send(self, msg):
        self.soc.sendall(msg.encode(encoding='utf-8'))


class chatServer:
    svrIP = '127.0.0.1'  # default
    port = 2500

    def __init__(self):
        self.server_soc = None
        self.room = room()

    def open(self):
        self.server_soc = socket.socket() # TCP socket (socket.AF_INET, socket.SOCK_STREAM)
        self.server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_soc.bind((chatServer.svrIP, chatServer.port))
        self.server_soc.listen()

    def run(self):
        self.open()
        print('Server Opened')

        while True:
            client_soc, addr = self.server_soc.accept()
            print(addr, 'Connected')
            c = chatClient(self.room, client_soc)
            self.room.addClient(c)
            th = threading.Thread(target=c.recv)
            th.start()

        self.server_soc.close()


def main():
    cs = chatServer()
    cs.run()


main()