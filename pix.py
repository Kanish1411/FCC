
import numpy as np
from PIL import Image
from khv import permRows,revPermRows,sf,isf
import time


def encrypt(file,key):
    rgb = file
    t = rgb.tolist()
    for _ in range(int(key,base=2)%100+6):
        t=permRows(t)
    for _ in range(1,int(key,base=2)%3+2):
        t=sf(t)
    cip = np.array(t,dtype=np.uint8)
    return cip

def decrypt(file,key):
    img = Image.open(file)
    rgb = np.array(img)
    p1 = rgb.tolist()
    for _ in range(1,int(key,base=2)%3+2):
        p1=isf(p1)
    for _ in range(int(key,base=2)%100+6):
        p1=revPermRows(p1)
    o = np.array(p1,dtype=np.uint8)
    #Image.fromarray(o,"RGB").save("output.png")
    return o
