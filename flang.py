import sys
import re
from typing import cast , Tuple

if len(sys.argv) < 2:
    print("usage:python flang.py file.flg")
    sys.exit(1)

slot = [b"\x00" for _ in range(3000)]
ptr = 0
jmpMap = {}
mapStack = []
jmpI = []
index = 0

#ハンドラここから

def inc():
    val = slot[ptr][0]
    slot[ptr] = bytes([(val + 1) % 256])
    
def dec():
    val = slot[ptr][0]
    slot[ptr] = bytes([(val - 1) % 256])

def ptf():
    global ptr
    ptr += 1
    
def ptb():
    global ptr
    ptr -= 1
    
def lpStr():
    global index
    if not slot[ptr][0]:
        index = jmpMap[index] + 1

def lpEnd():
    global index
    if slot[ptr][0]:
        index = jmpMap[index]

def prt():
    global slot,ptr
    sys.stdout.buffer.write(slot[ptr])
    sys.stdout.flush()

def ipt():
    global slot,ptr
    in_b = sys.stdin.buffer.read(1)
    if in_b:
        slot[ptr] = in_b
    else:
        slot[ptr] = b"\x00"

TABLE = {
    ("f","f","f"):inc,
    ("f","f","ff"):dec,
    ("f","ff","f"):ptf,
    ("f","ff","ff"):ptb,
    ("ff","f","f"):lpStr,
    ("ff","f","ff"):lpEnd,
    ("ff","ff","f"):prt,
    ("ff","ff","ff"):ipt
}

#ここまで

with open(sys.argv[1]) as file:
    PP = "".join(re.findall(r"ff|f|\n",file.read()))
    SPL = PP.split("\n")
    CODE_SET = [SPL[i:i+3] for i in range(0,len(SPL),3)]
    for i,code in enumerate(CODE_SET):
        if code == ["ff","f","f"]:
            mapStack.append(i)
        elif code == ["ff","f","ff"]:
            if not mapStack:
                print("\nerror not found match \"[\" at {} line".format(i*3))
            start = mapStack.pop()
            jmpMap[start] = i
            jmpMap[i] = start 
    if mapStack:
        print("error not found match \"]\" at {} line".format(i*3))

while len(CODE_SET) > index:
    code = cast(Tuple[str,str,str],tuple(CODE_SET[index]))
    if code in TABLE:
        TABLE[code]()
    else:
        print("error {} line instruction is not found".format(index*3))
    
    index += 1