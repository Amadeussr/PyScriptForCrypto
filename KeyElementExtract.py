import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

def ExtractHISFile(HISData):
    HISKeyList = HISData.columns.tolist()
    HISKeyStr = HISKeyList[0]
    '''
    TAG             Description                                         
    -----------------------------------------------------------------------------------        
    FF49            Header
    8X              X Byte(s) length information
    XX XX           Total length information(X byte(s))
    81              Modulus(n) tag
    8Y              Y Byte(s) Modulus length information
    XX              Modulus length information(Y byte(s))
    XX...XX         Modulus
    82              Public exponent(e) tag
    XX              Public exponent length information
    XX...XX         Exponent
    91              Private exponent(d) tag
    8Z              Private exponent length information
    XX              Private exponent length(Z byte(s))
    XX...XX         Private exponent
    '''
    #10 Header check 
    Offset = 0
    if HISKeyStr[Offset : Offset + 4] != "FF49":
        print("Header check failed, Invalid Input File!")
        return
    else:
        print("Valid header!")
        
    Offset += 4

    #20 Total length
    #21 Get total length format
    TotalLengthFormat = int(HISKeyStr[Offset : Offset + 2], 16) - 0x80
    Offset += 2
    #22 Get Mod accroding to the length format
    TotalLength = int(HISKeyStr[Offset : Offset + TotalLengthFormat * 2], 16)
    # print(hex(TotalLength))
    Offset += 2 * TotalLengthFormat

    #30 Extract Modulus(m)
    #31 Check the tag of Mod
    if HISKeyStr[Offset : Offset + 2] == "81":
        Offset += 2
        # Valid tag found, extract length format then Mod
        ModLengthFormat = int(HISKeyStr[Offset : Offset + 2], 16) - 0x80
        Offset += 2
        ModLength = int(HISKeyStr[Offset : Offset + ModLengthFormat * 2], 16)
        Offset += ModLengthFormat * 2
        # print(hex(ModLength))
        Mod = HISKeyStr[Offset : Offset + ModLength * 2]
        print("Modulus:", Mod, "length:", int(len(Mod)/2))
        Offset += ModLength * 2
    else:
        # No valid tag found
        print("no valid modulus tag!")
        return

    #40 Extract public Exp(e)
    #41 Check the tag of e
    if HISKeyStr[Offset : Offset + 2] == "82":
        Offset += 2
        # Valid tag found, extract public exp
        ExpLength = int(HISKeyStr[Offset : Offset + 2], 16)
        Offset += 2
        # print(hex(ExpLength))
        Exp = HISKeyStr[Offset : Offset + ExpLength * 2]
        print("Public Exp:", Exp, "length:", int(len(Exp)/2))
        Offset += ExpLength * 2
    else:
        # No valid tag found
        print("no valid public Exp tag!")
        return
    
    #50 Extract private Exp(d)
    #51 Check the tag of d
    if HISKeyStr[Offset : Offset + 2] == "91":
        Offset += 2
        # Valid tag found, extract length format then d
        DLengthFormat = int(HISKeyStr[Offset : Offset + 2], 16) - 0x80
        Offset += 2
        DLength = int(HISKeyStr[Offset : Offset + DLengthFormat * 2], 16)
        Offset += DLengthFormat * 2
        # print(hex(DLength))
        d = HISKeyStr[Offset : Offset + DLength * 2]
        print("Private Exp:", d, "length:", int(len(d)/2))
        Offset += DLength * 2
    else:
        # No valid tag found
        print("no valid private exp tag!")
        return



'''
Main implementation start
'''
print("Please select an input file!")
input_path = filedialog.askopenfilename()
# HISData = pd.read_csv(r'C:\Users\15424\Desktop\python\DemoKeys\key_dev.txt')
if input_path != "":
    HISData = pd.read_csv(input_path)
    ExtractHISFile(HISData)
else:
    print("Please select a valid path!")

