from socket import *
import sys
import os
import time

server_port = ('175.10.204.45', 9999)

sk = socket(AF_INET, SOCK_STREAM)

sk.connect(server_port)


def recvfile():  # 接受文件
    base_path = 'd:\\recvfiles'
    conn = sk
    pre_data = conn.recv(1024).decode()
    file_name, file_size = pre_data.split('|')
    conn.sendall('nothing'.encode())
    recv_size = 0
    file_dir = os.path.join(base_path, file_name)
    f = open(file_dir, 'wb')
    Flag = True
    while Flag:
        if int(file_size) > recv_size:
            data = conn.recv(1024)
            recv_size += len(data)
            f.write(data)
        else:
            recv_size = 0
            Flag = False

    print('recive succeeded.')
    sk.sendall("ok".encode())
    f.close()


def sendmsg():  # 发信息
    print("enter \"#exit#\" if you want to change mode or leave")
    while True:
        smsg = input()
        sk.sendall(smsg.encode())
        if smsg == "#exit#":
            break


def sendfile():  # 上传文件
    path = input('path:')
    file_name = os.path.basename(path)
    file_size = os.stat(path).st_size
    Informf = (file_name+'|'+str(file_size))
    sk.send(Informf.encode())
    sk.recv(1024)
    send_size = 0
    f = open(path, 'rb')
    Flag = True
    while Flag:
        if send_size + 1024 > file_size:
            data = f.read(file_size-send_size)
            Flag = False
        else:
            data = f.read(1024)
            send_size += 1024
        sk.send(data)
    f.close()
    sk.recv(1024)
    print('upload succeeded.')


def sends():
    while True:
        print("press 1 , 2 or 3 to choose:")
        sel = input('[1]send message [2]send file [3]recive file [4]exit\n')
        if sel == '1':
            sk.sendall("message".encode())
            sk.recv(1024)
            sendmsg()
        elif sel == '2':
            sk.sendall("file".encode())
            sk.recv(1024)
            sendfile()
        elif sel == '3':
            sk.sendall("recvfile".encode())
            print("files:")
            while True:
                names = sk.recv(1024).decode()
                if names == '1':
                    needfile = input("which one:")
                    sk.sendall(needfile.encode())
                    recvfile()
                    break
                sk.sendall("ok".encode())
                print(names)  # 先列出所有已上传的文件
        elif sel == '4':
            sk.sendall("exit".encode())
            time.sleep(1)
            break
        else:
            print("please enter 1 , 2 or 3!")


sends()

sk.close()
