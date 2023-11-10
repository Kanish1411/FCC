import socket
import sympy
from pix import decrypt
import time
import numpy as np
"""s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((socket.gethostname(),6000))
t1=time.time()
k=None
msg=s.recv(2048)
msg=str(msg)
msg=msg[2:len(msg)-1]
b=msg.split("-")
g=int(b[0])
p=int(b[1])
print(b)
x=sympy.randprime(0,1000)
y=(g**x)%p
print("y:",y)
s.send(bytes(str(y),"utf-8"))
xf=s.recv(2048)
xf=int(xf)
print(xf)
yf=(xf**x)%p
print(yf)
k=yf
k=(k**4)%(2**32)
print("k:",k)
print(bin(k),len(str(bin(k))))
key=str(bin(k))[2:]
while len(key)<32:
    key="1"+key
u=True
while u:
    fs = s.recv(2048).decode('utf-8', 'ignore')
    fi = open("file.png", "wb")
    print("receiving file...")
    fib = b""
    done = False
    while not done:
        data = s.recv(1024)
        if fib[-5:] == b"<END>":
            done = True
        else:
            fib += data
    fi.write(fib[:-5])
    t2 = time.time()
    print(t2 - t1)
    fi.close()
    print("received")
    a = decrypt("file.png", key)
    s.sendall("yeah".encode('utf-8'))

"""

import socket
import os
import cv2
import sympy
import numpy as np

def generate_key():
    # Generate a shared key using the Diffie-Hellman key exchange
    t = base()
    g, p = t[0], t[1]
    x = sympy.randprime(0, 1000)
    y = (g ** x) % p
    return str((y ** 4) % (2 ** 32))

def receive_images(output_folder, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), port))
    s.listen(1)

    print(f"Listening for connections on port {port}")

    cli_soc, addr = s.accept()
    print("Connection made with", addr)

    # Receive and ignore the encryption key (as it's generated on both sides)
    cli_soc.recv(2048).decode('utf-8')

    while True:
        # Receive the image size
        img_size = int(cli_soc.recv(2048).decode('utf-8'))

        if img_size == 0:
            break  # End of image transmission

        # Receive the image data
        img_data = cli_soc.recv(img_size)
        img = np.frombuffer(img_data, dtype=np.uint8)

        # Save the received image
        output_path = os.path.join(output_folder, f"received_{time.time()}.png")
        cv2.imwrite(output_path, img)

        # Send acknowledgment to the sender
        cli_soc.send("Image received successfully".encode('utf-8'))

    cli_soc.close()

# Example usage
output_folder = "output"
receiver_port = 6000

receive_images(output_folder, receiver_port)

