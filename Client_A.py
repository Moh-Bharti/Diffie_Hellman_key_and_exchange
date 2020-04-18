import socket
import hashlib
import hmac
import random
mod_p = 17359

secret = 5544
da = 12 #random.randint(2,mod_p-2)
alpha = 31
beta = (alpha**da)%mod_p

def share_secret(A):
    base_g = primitive(mod_p)
    secret = (A**alpha) % mod_p
    return secret

def primitive(pri):
    p = pri - 2
    pr = pri
    for i in range(p, 2, -2):
        if (i ** (p + 1)) % pri == 1:
            pr = i

            break
    return pr


def connect():

    host = '127.0.0.1'  # The server's hostname or IP address

    port = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host,port))
        s.listen(1)
        conn, addr = s.accept()

        y = 0
        u = 0
        with conn:
            print('Connected by', addr)
            while y<5:
                if y == 0: # Sending the public key to Client B
                    print("-----------Sending public key message--------------")
                    message = str(alpha)+" "+str(beta)+" "+MAC(str(alpha).encode())+" "+MAC(str(beta).encode())
                    conn.sendall(bytes(message.encode()))
                    print(message)
                    u = 1
                elif y == 1: # Receiving Authenticate message
                    data = conn.recv(1024)
                    print("-------------Receiving Authentication message--------------- ")
                    print(data.decode("utf-8"))
                    if data.decode("utf-8") != "Got the key":
                        break
                    else:
                        u = 1
                elif y == 2:
                    data = conn.recv(1024)
                    st = decrypt(data.decode("utf-8"),mod_p)
                    print("Received message: ",st)
                elif y == 3:
                    data = conn.recv(1024)
                    st = decrypt(data.decode("utf-8"), mod_p)
                    print("Received message: ",st)
                else:
                    data = conn.recv(1024)
                    st = decrypt(data.decode("utf-8"), mod_p)
                    print("Received message: ",st)
                y += u

        print("Connection closed")


def MAC(message):
    digester = hmac.new(bytes(secret), message, hashlib.sha1)
    digest = digester.hexdigest()

    return digest


def decrypt(message,p):

    dec_mess = message.split()
    mess = dec_mess[0]
    key = int(dec_mess[1])
    has = dec_mess[2]
    ori_mess = ""
    for i in range(len(mess)):

        ori_mess += chr(((ord(mess[i])%p)*(key**(p-1-da))%p)%p)

    if MAC(ori_mess.encode()) == has:
        return ori_mess
    else:

        return "Nothing"


if __name__=='__main__':
    print("Starting the Communication.............. ")

    connect()
