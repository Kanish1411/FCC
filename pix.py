
import numpy as np
from PIL import Image
from khv import enc,dec,permRows,revPermRows,sf,isf
import time


def encrypt(file,key):
    rgb = file
    t = rgb.tolist()
    print("loop:",int(key,base=2)%100+6,"sf:",int(key,base=2)%3+2)
    for i in range(int(key,base=2)%100+6):
        t=permRows(t)
    for i in range(1,int(key,base=2)%3+2):
        t=sf(t)
    cip = np.array(t,dtype=np.uint8)
    """ imo = Image.fromarray(cip, 'RGB')
    imo.save('After_enc.png')"""
    return cip

def decrypt(file,key):
    img = Image.open(file)
    rgb = np.array(img)
    p1 = rgb.tolist()
    for i in range(1,int(key,base=2)%3+2):
        p1=isf(p1)
    for i in range(int(key,base=2)%100+6):
        p1=revPermRows(p1)
    o = np.array(p1,dtype=np.uint8)
    Image.fromarray(o,"RGB").save("output.png")
    return o
