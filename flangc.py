import sys
import re
import os

if len(sys.argv) < 2:
    print("usage:python flang.py file.flg")
    sys.exit(1)
    
TABLE = {
    ("f","f","f"):"+",
    ("f","f","ff"):"-",
    ("f","ff","f"):">",
    ("f","ff","ff"):"<",
    ("ff","f","f"):"[",
    ("ff","f","ff"):"]",
    ("ff","ff","f"):".",
    ("ff","ff","ff"):","
}
    
with open(sys.argv[1]) as file:
    PP = "".join(re.findall(r"ff|f|\n",file.read()))
    SPL = PP.split("\n")
    CODE_SET = [SPL[i:i+3] for i in range(0,len(SPL),3)]
    with open(os.path.splitext(os.path.basename(sys.argv[0]))[0] + ".bf","w") as file:
        file.write("".join([TABLE.get(tuple(i)) for i in CODE_SET]))