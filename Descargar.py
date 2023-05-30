#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 15:46:46 2023

@author: erick
"""


import os
import requests

if not os.path.exists("Data"):
    os.makedirs("Data")
    

def desencriptar(texto, llave):
    _desencriptado = ""
    _abc = ["Y", "F", "4", "D", "é", "z", "J", "H", "u", "V", "y", "Q", "Z",
            "P", "Ó", "\n", "_", "ú", "á", "i", "p", "r", "A", "ü", "n", ",", 
            "l", "Ú", "9", "x", "R", "b", "t", "Á", "o", "I", "Ü", "B", "S", 
            "X", "L", "d", "1", "0", "O", "c", "N", "T", "í", "É", "3", "e", 
            "v", "K", "-", "U", "W", "2", "f", "a", "C", "g", "G", " ", "j", 
            "k", "ó", "7", "Í", "s", "5", "E", "h", "8", "M", "m", ".", "ñ", 
            "6", "q", "+", "?"
           ]
    
    for i, l in enumerate(texto):
        k = int(llave[i % len(llave)])
        _desencriptado += _abc[(_abc.index(l) - k) % len(_abc)]
        
    return _desencriptado

response = requests.get("https://raw.githubusercontent.com/ErickdeMauleon/data/main/file.txt")
BQ_body = response.text

with open("Data/BQ.csv", "w") as file:
    _llave = "60929458407514816627840059651106250515800606449794710738366456305812117044244541632935921593492810116860315026074700708144858641851798889"
    file.write(desencriptar(BQ_body, _llave))