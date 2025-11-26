import ctypes
import time
import pandas as pd

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    dwFlags=0x0001 if hexKeyCode==0x48 or hexKeyCode==0x50 or hexKeyCode==0x4B or hexKeyCode==0x4D else 0x0008
    ii_.ki = KeyBdInput( 0, hexKeyCode, dwFlags, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    dwFlags=0x0001 if hexKeyCode==0x48 or hexKeyCode==0x50 or hexKeyCode==0x4B or hexKeyCode==0x4D else 0x0008
    ii_.ki = KeyBdInput( 0, hexKeyCode, dwFlags | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

# w:0x11 a:0x1E s:0x1F d:0x20 ↑:0x48 ↓:0x50 ←:0x4B →:0x4D shift:0x2A space:0x39

graphemes={
    'x':[0x11,0x48,0x39],'aa':[0x11,0x50,0x39],'ee':[0x11,0x4B,0x39],'pp':[0x11,0x4D,0x39],
    'cj':[0x1E,0x48,0x39],'ej':[0x1E,0x50,0x39],'sj':[0x1E,0x4B,0x39],'hj':[0x1E,0x4D,0x39],
    'r':[0x1F,0x48,0x39],'ra':[0x1F,0x50,0x39],'re':[0x1F,0x4B,0x39],'w':[0x1F,0x4D,0x39],
    'si':[0x20,0x48,0x39],'ai':[0x20,0x50,0x39],'ei':[0x20,0x4B,0x39],'su':[0x20,0x4D,0x39],
    's':[0x48,0x39],'hh':[0x50,0x39],'hm':[0x4B,0x39],'f':[0x4D,0x39],
    'l':[0x11,0x39,0x48],'ax':[0x11,0x39,0x50],'ex':[0x11,0x39,0x4B],'ux':[0x11,0x39,0x4D],
    'cx':[0x1E,0x39,0x48],'er':[0x1E,0x39,0x50],'sx':[0x1E,0x39,0x4B],'hu':[0x1E,0x39,0x4D],
    'k':[0x1F,0x39,0x48],'ka':[0x1F,0x39,0x50],'ke':[0x1F,0x39,0x4B],'ku':[0x1F,0x39,0x4D],
    't':[0x20,0x39,0x48],'ta':[0x20,0x39,0x50],'te':[0x20,0x39,0x4B],'tu':[0x20,0x39,0x4D],
    'p':[0x39,0x48],'h':[0x39,0x50],'he':[0x39,0x4B],'pu':[0x39,0x4D],
    'ji':[0x2A,0x11,0x48,0x39],'ja':[0x2A,0x11,0x50,0x39],'je':[0x2A,0x11,0x4B,0x39],'ju':[0x2A,0x11,0x4D,0x39],
    'q':[0x2A,0x1E,0x48,0x39],'qa':[0x2A,0x1E,0x50,0x39],'qe':[0x2A,0x1E,0x4B,0x39],'o':[0x2A,0x1E,0x4D,0x39],
    'v':[0x2A,0x1F,0x48,0x39],'am':[0x2A,0x1F,0x50,0x39],'y':[0x2A,0x1F,0x4B,0x39],'in':[0x2A,0x1F,0x4D,0x39],
    'z':[0x2A,0x20,0x48,0x39],'a':[0x2A,0x20,0x50,0x39],'e':[0x2A,0x20,0x4B,0x39],'zu':[0x2A,0x20,0x4D,0x39],
    'i':[0x2A,0x48,0x39],'a-':[0x2A,0x50,0x39],'e-':[0x2A,0x4B,0x39],'u':[0x2A,0x4D,0x39],
    'li':[0x2A,0x11,0x39,0x48],'la':[0x2A,0x11,0x39,0x50],'le':[0x2A,0x11,0x39,0x4B],'lu':[0x2A,0x11,0x39,0x4D],
    'ch':[0x2A,0x1E,0x39,0x48],'qr':[0x2A,0x1E,0x39,0x50],'sh':[0x2A,0x1E,0x39,0x4B],'ao':[0x2A,0x1E,0x39,0x4D],
    'g':[0x2A,0x1F,0x39,0x48],'ga':[0x2A,0x1F,0x39,0x50],'ge':[0x2A,0x1F,0x39,0x4B],'gu':[0x2A,0x1F,0x39,0x4D],
    'd':[0x2A,0x20,0x39,0x48],'da':[0x2A,0x20,0x39,0x50],'de':[0x2A,0x20,0x39,0x4B],'du':[0x2A,0x20,0x39,0x4D],
    'b':[0x2A,0x39,0x48],'ba':[0x2A,0x39,0x50],'be':[0x2A,0x39,0x4B],'bu':[0x2A,0x39,0x4D]
    }

def GetSamePrefixesNum(list:list,index:int,searchList:list):
    prefixes=0
    if index!=len(hexKeyCodesList)-1:
        flag=index
        while (flag+1<len(hexKeyCodesList)):
            flag+=1
            for i,j in enumerate(hexKeyCodesList[index]):
                if j!=hexKeyCodesList[flag][i]:
                    prefixes=0
            prefixes+=1
    

def PressKeyButtens(hexKeyCodesList:list):
    if len(hexKeyCodesList)==2:
        PressKey(hexKeyCodesList[0])
        time.sleep(0.16)
        PressKey(hexKeyCodesList[1])
        time.sleep(0.08)
        ReleaseKey(hexKeyCodesList[1])
        ReleaseKey(hexKeyCodesList[0])
    elif len(hexKeyCodesList)==3:
        PressKey(hexKeyCodesList[0])
        time.sleep(0.24)
        PressKey(hexKeyCodesList[1])
        time.sleep(0.16)
        PressKey(hexKeyCodesList[2])
        time.sleep(0.08)
        ReleaseKey(hexKeyCodesList[2])
        ReleaseKey(hexKeyCodesList[1])
        ReleaseKey(hexKeyCodesList[0])
    elif len(hexKeyCodesList)==4:
        PressKey(hexKeyCodesList[0])
        time.sleep(0.32)
        PressKey(hexKeyCodesList[1])
        time.sleep(0.24)
        PressKey(hexKeyCodesList[2])
        time.sleep(0.16)
        PressKey(hexKeyCodesList[3])
        time.sleep(0.08)
        ReleaseKey(hexKeyCodesList[3])
        ReleaseKey(hexKeyCodesList[2])
        ReleaseKey(hexKeyCodesList[1])
        ReleaseKey(hexKeyCodesList[0])



if __name__ == "__main__":
    df = pd.read_csv('GingerDictionary.csv')
    mode=input('Select Mode(1/2):1.Input All Words 2.Input Words: ')
    if mode=='1': 
        hexKeyCodesList=[]
        for index, row in df.iterrows():
            hexKeyCodesList.append([graphemes[i] for i in row['graphemes'].split(' ')])
        print('Input words after 5 seconds...')
        time.sleep(5) #time to switch to the game window
        for index,i in enumerate(hexKeyCodesList):
            for graphemes in i:
                PressKeyButtens(graphemes)
                time.sleep(0.25) #wait between graphemes
            time.sleep(0.2) #wait between words
    elif mode=='2':
        wordDict={}
        for index, row in df.iterrows():
            wordDict[row['word']]=[graphemes[i] for i in row['graphemes'].split(' ')]
        print('Input a word or word list(split by space) [input "exit" to quit]')
        while True:
            wordList=input()
            if wordList=='exit':
                break
            hexKeyCodesList=[]
            for word in wordList.split(' '):
                if word in wordDict:
                    hexKeyCodesList.append(wordDict[word])
                else:
                    print(f'Word "{word}" not found in dictionary')
                    continue
            print('Input words after 3 seconds...')
            time.sleep(3) #time to switch to the game window
            for index,i in enumerate(hexKeyCodesList):
                for graphemes in i:
                    PressKeyButtens(graphemes)
                    time.sleep(0.25) #wait between graphemes








