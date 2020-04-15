import socket
import hashlib
import hmac

prime = 17377

mod_p = 17359

prive = 23

def share_secret(B):
    base_g = primitive(mod_p)
    share = (B**prive) % mod_p


def primitive(pri):
    p = pri-2
    pr = pri

    for i in range(p,2,-2):
        if (i**(p+1))% pri == 1:
            pr = i

     
            break

    return pr




def connect():
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
                print("Got it : ", repr(data))


if __name__ == '__main__':
    print("hrllo")
    print(primitive(prime))

