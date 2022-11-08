from socket import *

server_name = '127.0.0.1'

server_port = 12000

client_socket = socket(AF_INET, SOCK_DGRAM)

message = input("input lowercase sentence")

client_socket.sendto(message.encode(), (server_name, server_port))

modified_message, server_address = client_socket.recvfrom(2048)

print(modified_message.decode())

client_socket.close()
