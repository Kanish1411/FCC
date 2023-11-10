import socket
import sympy
import os
from diffieSender import base
from pix import encrypt
import time
import cv2
"""s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),6000))
s.listen(1)
k=None
t1=time.time()
while True:
    cliSoc,addr=s.accept()
    print("connection made with ",addr)
    t=base()
    g,p=t[0],t[1]
    cliSoc.send(bytes(str(t[0])+"-"+str(t[1]),"utf-8"))
    x=sympy.randprime(0,1000)
    y=(g**x)%p
    print("y:",y)
    cliSoc.send(bytes(str(y),"utf-8"))
    xf=cliSoc.recv(2048)
    xf=int(xf)
    print(xf)
    yf=(xf**x)%p
    print(yf)
    k=yf
    break
k=(k**4)%(2**32)
print("k:",k)
print(bin(k),len(str(bin(k))))
key=str(bin(k))[2:]
while len(key)<32:
    key="1"+key

video_path = "video.mp4"
output_directory = "encrypt"
video = cv2.VideoCapture(video_path)
count = 0
print("asdad")
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

while True:
    success, frame = video.read()
    if not success:
        break
    encrypted_frame = encrypt(frame,key)
    fname = f"{count}.png"
    frame_path = os.path.join(output_directory, fname)
    cv2.imwrite(frame_path, encrypted_frame)
    count += 1
    fi=open(frame_path,"rb")
    fs=os.path.getsize(frame_path)
    cliSoc.send(str(fs).encode())
    data=fi.read()
    cliSoc.sendall(data)
    cliSoc.send(b"<END>")
    cliSoc.settimeout(15)
    ack = cliSoc.recv(2048).decode('utf-8')
    print(ack)
video.release()
t2=time.time()
print(t2-t1)
fi.close()
print("sent")
cliSoc.close()
import socket
import os
from diffieSender import base
import time
import cv2

def generate_key():
    # Generate a shared key using the Diffie-Hellman key exchange
    t = base()
    g, p = t[0], t[1]
    x = sympy.randprime(0, 1000)
    y = (g ** x) % p
    return str((y ** 4) % (2 ** 32))

def send_images(folder_path, host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Generate and send the encryption key
    key = generate_key()
    s.send(bytes(key, "utf-8"))

    # Get the list of image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)

        # Read the image
        img = cv2.imread(image_path)

        # Send the image size
        img_size = os.path.getsize(image_path)
        s.send(str(img_size).encode())

        # Send the image data
        s.sendall(img.tobytes())

        # Wait for acknowledgment from the receiver
        ack = s.recv(2048).decode('utf-8')
        print(ack)

    # Signal the end of image transmission
    s.send(b"<END>")
    s.close()

# Example usage
folder_path = "encrypt"
receiver_host = "127.0.0.1"
receiver_port = 6000
send_images(folder_path, receiver_host, receiver_port)
"""

video_path = "video.mp4"
output_directory = "encrypt"
video = cv2.VideoCapture(video_path)
count = 0
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

while True:
    success, frame = video.read()
    if not success:
        break
    encrypted_frame = frame
    fname = f"{count}.png"
    frame_path = os.path.join(output_directory, fname)
    cv2.imwrite(frame_path, encrypted_frame)
    count+=1

