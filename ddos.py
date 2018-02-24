import socket
import argparse
from threading import Thread

socketList = []
# 命令格式'#-H xxx.xxx.xxx.xxx -p xxxx -c <start|stop>'
# 发送命令


def sendCmd(cmd):
    print('Send command......')
    for sock in socketList:
        sock.send(cmd.encode('utf-8'))

# 等待连接


def waitConnect(s):
    while True:
        sock, addr = s.accept()
        if sock not in socketList:
            socketList.append(sock)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 58868))
    s.listen(1024)
    t = Thread(target=waitConnect, args=(s,))
    t.start()

    print('Wait at least a client connection!')
    while not len(socketList):
        pass
    print('It has been a client connection!')

    while True:
        print('=' * 50)
        print('The command format:"#-H xxx.xxx.xxx.xxx -p xxxx -c <start>"')
        # 等待输入命令
        cmd_str = input('Please input cmd:')
        if len(cmd_str):
            if cmd_str[0] == '#':
                sendCmd(cmd_str)


if __name__ == '__main__':
    main()
