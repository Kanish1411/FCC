import socket 
import os,cv2,sympy,time,pickle
from diffieSender import base
from pix import encrypt

port=6000
server=socket.gethostbyname(socket.gethostname())
addr=(server,port)
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
s.listen(1)
key=0
done=0
def videofram(a):
    global done
    video_path = a
    output_directory = "encrypt"
    video = cv2.VideoCapture(video_path)
    count = 0
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    while True:
        success, frame = video.read()
        if not success:
            break
        encrypted_frame = encrypt(frame,key)
        fname = f"{count}.png"
        frame_path = os.path.join(output_directory, fname)
        cv2.imwrite(frame_path,encrypted_frame)
        count+=1
def setup(soc):
    global key
    t=base()
    g,p=t[0],t[1]
    soc.send(bytes(str(g)+"-"+str(p),"utf-8"))
    x=sympy.randprime(0,1000)
    y=(g**x)%p
    soc.send(bytes(str(y),"utf-8"))
    xf=soc.recv(2048)
    xf=int(xf)
    yf=(xf**x)%p
    k=yf
    k=(k**4)%(2**32)
    key=str(bin(k))[2:]
    while len(key)<32:
        key="1"+key
    
def sendframes(soc, directory):
    frame_number = 0
    for filename in sorted(os.listdir(directory), key=lambda x: int(x.split('.')[0])):
        if filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                frame_data = {'frame_number': frame_number, 'image_data': image_data}
                frame_pickle = pickle.dumps(frame_data)
                soc.sendall(len(frame_pickle).to_bytes(4, byteorder='big'))
                soc.sendall(frame_pickle)
                frame_number += 1
    soc.sendall(b"<END>")
while True:
    soc,add=s.accept()
    inp=input("enter video name")
    if not os.path.exists(inp):
        print("file not found")
        break
    t=time.time()
    setup(soc)
    t1=time.time()
    print("Socket",t1-t)
    videofram(inp)
    t2=time.time()
    print("Videoframe",t2-t1)
    sendframes(soc,"encrypt")
    t3=time.time()
    print("send",t3-t2)
    print("full",t3-t)
    exit()
soc.close()