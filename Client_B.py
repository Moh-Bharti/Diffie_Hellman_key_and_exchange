import socket
import hashlib
import hmac
import random



mod_p = 17359

B_private = 12
alpha = 0
beta = 0
secret = 5544



def MAC(message):

    digester = hmac.new(bytes(secret),message,hashlib.sha1)
    print(secret)
    digest = digester.hexdigest()
    return digest


def primitive(pri):
    p = pri-2
    pr = pri

    for i in range(p, 2 , -2):
        if (i**(p+1))% pri == 1:
            pr = i

     
            break

    return pr


g = primitive(mod_p)


def connect():
    try:
        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Communicating.................")
            s.connect((HOST,PORT))

            i = 0
            while i < 7:
                if i == 0:
                    data = s.recv(1024)

                    d = int(data.decode("utf-8"))
                    print()
                    print("-------Receiving public message from Client_A and Computing the shared secret----------")
                    global secret
                    secret = (d ** B_private) % mod_p
                    print("Shared Secret:   ", secret)

                elif i == 1:
                    print()
                    print("----Sending Client_A a public message-----")
                    string = str((g**B_private)%mod_p)
                    s.sendall(bytes(string.encode()))

                elif i == 2:
                    data = s.recv(1024)
                    print()
                    print("Receiving the message:  ",repr(data))
                    alpha, beta = verify(data.decode("utf-8"))
                elif i == 3:
                    print()
                    print("-----------Sending the conformation message-----------")

                    if alpha == 1 and beta == 1:
                        s.sendall(bytes("Not Got".encode()))
                    else:
                        s.sendall(bytes("Got the key".encode()))
                elif i == 4:
                    print()
                    print("Sending message: hello 1")

                    s.sendall(bytes(encrypt("hello 1",alpha,mod_p,beta).encode()))
                elif i == 5:
                    print()
                    print("Sending message: hello 2")

                    s.sendall(bytes(encrypt("hello 2",alpha,mod_p,beta).encode()))
                else:
                    print()
                    print("Sending message: hello 3")

                    s.sendall(bytes(encrypt("hello 3",alpha,mod_p,beta).encode()))
                i += 1

            print()
            print(".........Closing Connection........... ")
    except ConnectionAbortedError:
        print()


def encrypt(message, alpha, p, beta):
    k = random.randint(2, p - 2)
    enc_mess = ""
    for i in range(len(message)):
        enc_mess += chr((ord(message[i]) * (beta ** k)) % p)

    hashes = MAC(message.encode())
    enc_mess += " " + str((alpha ** k) % p)

    payload = enc_mess + " " + hashes

    return payload


def verify(message):
    mess = message.split()

    if MAC(mess[0].encode()) == mess[2] and MAC(mess[1].encode()) == mess[3]:
        alpha1 = int(mess[0])
        beta1 = int(mess[1])

        return alpha1,beta1

    else:
        alpha2 = 1
        beta2 =1
        return alpha2,beta2


if __name__ == '__main__':

    connect()




