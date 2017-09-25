#-*-coding=utf-8-*-
from BLL import InvokeBll
import socket


if __name__=="__main__":
    try:
        InvokeBll.ph_bll().Launch_Page()
    except socket.error,ex:
        print('执行结束！'+ex.message)
