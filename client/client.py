from socket import socket
from msgutils import recv_msg, send_msg, default_encoding

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 12347

    with socket() as sock:
        sock.connect((ip, port))

        while True:
            recvMsg = recv_msg(sock)
            if not recvMsg:
                print('No msg! Disconnected!')
                break
            choice = input(recvMsg.decode(default_encoding))

            send_msg(choice.encode(default_encoding), sock)

            if choice == '0':
                print('disconnected. bye-bye!')
                break
