from socket import *

server_port = 12000

server_socket = socket(AF_INET, SOCK_STREAM)

server_socket.bind(('', server_port))

server_socket.listen(1)

print("I'm ready, go on.")

while 1:
    connection_socket, addr = server_socket.accept()
    message = connection_socket.recv(1024)
    modified_message = message.decode().upper()
    connection_socket.send(modified_message.encode())
    connection_socket.close()

print("server accidently closed.")
