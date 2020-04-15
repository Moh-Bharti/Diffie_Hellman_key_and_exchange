import socket
import hashlib
import hmac

mod_p = 17359


def primitive(pri):
    p = pri - 2
    pr = pri

    for i in range(p, 2, -2):
        if (i ** (p + 1)) % pri == 1:
            pr = i

            break

    return pr

def connect():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall('Hello, world I am  daiku'.encode())
        data = s.recv(1024)

    print('Received :  ', repr(data))

if __name__=='__main__':
    