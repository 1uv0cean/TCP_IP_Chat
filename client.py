#-*- coding:utf-8 -*-
from tkinter import *
from threading import *
import socket
import time

ip = "127.0.0.1" # default IP
port = 2500 # default Port
username = ""
global f
f = True

class Main:
    def __init__(self, Ui): # GUI 구성
        self.ui = Ui
        Ui.geometry("400 * 600")
        self.mainFrame = Frame(self.ui)
        self.mainFrame.pack(fill = X)

        self.subFrame1 = Frame(self.mainFrame)
        self.subFrame1.pack(fill = X)

        self.text = Text(self.subFrame1)
        self.scroll = Scrollbar(self.subFrame1)
        self.scroll.pack(side = RIGHT, fill = Y)
        self.text.config(width = 56, height =38)
        self.subFrame2 = Frame(self.mainFrame)
        self.subFrame2.pack(fill = X)



        