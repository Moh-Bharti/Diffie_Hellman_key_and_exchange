# Diffie_Hellman_key_and_exchange
Communication using Diffie Hellman and Elgmal Cryptosystem.
Communication protocol uses two keys and the protocol is----

First step Authentication:
Create Hash using HMAC Algorithm where the hash is encrypted using shared secret between the two nodes.
This hash is checked with the message received.

Second step Confidentiality:
For this Elgamal Cryptosystem is used which encypt the message and create the cyphertext.
The cyphertext is used to find the shared secret called session key.
Message is send between only B to A.
