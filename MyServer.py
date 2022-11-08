import socketserver
import sys
import os


clientlist = []

file_names = []

file_paths = []

user_name = ["Client1", "Client2"]

dir_path = 'D:\\temp'

remind_files = os.listdir(dir_path)

for file in remind_files:
    file_names.append(file)
    file_paths.append("{}\\{}".format(dir_path, file))


class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        conn = self.request
        clientlist.append(self.client_address)
        print('{} connect successfully.'.format(
            user_name[clientlist.index(self.client_address)]))
        outFlag = True
        while outFlag:
            mysign = clientlist.index(self.client_address)
            data = conn.recv(1024).decode()
            if data == 'exit':  # 用户断开连接
                outFlag = False
                print("{} has disconnected.".format(
                    user_name[clientlist.index(self.client_address)]))
                clientlist.pop(clientlist.index(self.client_address))
            elif data == 'message':  # 用户发送信息
                conn.sendall("ok".encode())
                while True:
                    recvmsg = conn.recv(1024).decode()
                    if recvmsg == "#exit#":
                        break
                    print("{}:{}".format(
                        user_name[mysign], recvmsg))
            elif data == 'file':  # 用户上传文件
                conn.sendall("ok".encode())
                base_path = 'D:\\temp'
                pre_data = conn.recv(1024).decode()
                file_name, file_size = pre_data.split('|')
                file_names.append(file_name)
                file_paths.append("{}\\{}".format(base_path, file_name))
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

                print('{} has uploaded a file.'.format(
                    user_name[mysign]))
                f.close()
                conn.sendall("ok".encode())
            elif data == 'recvfile':  # 用户请求下载文件
                for name in file_names:
                    conn.sendall("{}".format(name).encode())
                    conn.recv(1024)
                conn.sendall("1".encode())
                path = file_paths[file_names.index(conn.recv(1024).decode())]
                file_name = os.path.basename(path)
                file_size = os.stat(path).st_size
                Informf = (file_name+'|'+str(file_size))
                conn.send(Informf.encode())
                conn.recv(1024)
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
                    conn.send(data)
                f.close()
                conn.recv(1024)


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('175.10.204.45', 9999), MyServer)
    server.serve_forever()
