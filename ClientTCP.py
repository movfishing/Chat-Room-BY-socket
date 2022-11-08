from socket import *

server_name = '127.0.0.1'

server_port = 12000

client_socket = socket(AF_INET, SOCK_STREAM)

client_socket.connect((server_name, server_port))

message = input("input lowercase sentence:")

client_socket.send(message.encode())

modified_message = client_socket.recv(1024)

print(modified_message.decode())

client_socket.close()
