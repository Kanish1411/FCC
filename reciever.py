import socket
import sympy
from pix import decrypt
import time,cv2,pickle,os
import numpy as np
def receiveframes(soc, output_directory):
    frame_number = 0
    buffer_size = 4096
    buffer = b""
    while True:
        data_len_bytes = soc.recv(4)
        if not data_len_bytes:
            break
        data_len = int.from_bytes(data_len_bytes, byteorder='big')
        remaining_data = data_len - len(buffer)

        while remaining_data > 0:
            chunk = soc.recv(min(remaining_data, buffer_size))
            if not chunk:
                break
            buffer += chunk
            remaining_data -= len(chunk)

        if len(buffer) == data_len:
            frame_data = pickle.loads(buffer)
            filename = f"received_frame_{frame_data['frame_number']}.png"
            frame_path = os.path.join(output_directory, filename)
            with open(frame_path, "wb") as image_file:
                image_file.write(frame_data['image_data'])
            print(f"Received {filename}")
            buffer = b""  # Reset buffer for the next frame

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 6000))
t1 = time.time()
k = None
msg = s.recv(2048)
msg = str(msg)
msg = msg[2:len(msg) - 1]
b = msg.split("-")
g = int(b[0])
p = int(b[1])
print(b)
x = sympy.randprime(0, 1000)
y = (g ** x) % p
print("y:", y)
s.send(bytes(str(y), "utf-8"))
xf = s.recv(2048)
xf = int(xf)
print(xf)
yf = (xf ** x) % p
print(yf)
k = yf
k = (k ** 4) % (2 ** 32)
print("k:", k)
print(bin(k), len(str(bin(k))))
key = str(bin(k))[2:]
while len(key) < 32:
    key = "1" + key
u = True
output_directory = "received_frames"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
while u:
    receiveframes(s, output_directory)
    """fs = s.recv(2048).decode('utf-8', 'ignore')
    fi = open("file.png", "wb")
    print("receiving file...")
    header = s.recv(8).decode('utf-8')

    # Check if the header is correct
    if header != "199255":
        print("Invalid header")
        continue

    # Create a file to write the received image data
    fi = open("file.png", "wb")

    print("Receiving file...")
    fib = b""
    done = False
    while not done:
        data = s.recv(1024)
        if data[-5:] == b"<END>":
            done = True
        else:
            fib += data

    fi.write(fib[:-5])
    fi.close()
    print("Received")

     print(f"Received data: {fib[:50]}")
    fi.write(fib[:-5])
    t2 = time.time()
    print(t2 - t1)
    fi.close()
    print("received")
    a = decrypt("file.png", key)"""

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

"""