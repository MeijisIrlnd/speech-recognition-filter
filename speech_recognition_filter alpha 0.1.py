#Structure: 
import speech_recognition as sr
import csnd6
import win32com.client as wincl
import re
import Tkinter as tk
def speech_rec(): 
    r = sr.Recognizer()
    #with sr.AudioFile(AUDIO_FILE) as source:
    with sr.Microphone() as source:
        audio = r.listen(source)
    words = r.recognize_google(audio)
    return words

def cs_Perform():
    c.Perform()
    root = tk.Tk()
    button1 = tk.Button(root, text="Speech", command=speech_rec)
    button1.pack()
    state = str(button1.Button["state"])
    if state != "disabled":
        #reassign words array, this needs to work in a loop. 
    c.Stop()

speak = wincl.Dispatch("SAPI.SpVoice")

AUDIO_FILE = "D:\College\Csound Command 2.wav"

orc = """
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1
kFreq chnget "cutoff"
SLoc chnget "loc"
print 100
aSig vco2 0.5, 80
;aSig, aSig diskin  SLoc
aFilt moogladder aSig, kFreq, 0.5
outs aFilt, aFilt
endin

instr 2 
iLowF chnget "lowfreq"
iHighF chnget "highfreq"
iTime chnget "time"
SLoc chnget "loc"
kSweep line iLowF, iTime, iHighF
aSig vco2 0.5, 80
;aSig, aSig diskin SLoc
aFilt moogladder aSig, kSweep, 0.5
outs aFilt, aFilt
endin

instr 3
iRes chnget "res"
SLoc chnget "loc"
aSig vco2 0.5, 80
;aSig, aSig diskin SLoc
aFilt moogladder aSig, 200, iRes
outs aFilt, aFilt
endin

instr 4
iResLow chnget "reslow"
iResHigh chnget "reshigh"
iResTime chnget "restime"
SLoc chnget "loc"
kSweep line iResLow, iResTime, iResHigh
aSig vco2 0.5, 80
;aSig, aSig diskin SLoc
aFilt moogladder aSig, 200, kSweep
outs aFilt, aFilt
endin
"""

words = speech_rec()
nums = [int(s) for s in words.split() if s.isdigit()]
floats = re.findall('\d+(\.\d+)?', words)
print(floats)
print(nums)
split = words.split()
print(split)
c = csnd6.Csound()
c.SetOption("-odac")
c.SetOption("-m7")
c.CompileOrc(orc)
if "set" in split:
    if "cut" in split:
        sco = "i1 0 [60*60*24*7]"
    elif "resonance" in split:
        sco = "i3 0 [60*60*24*7]"
elif "sweep" in split:
    if "cut" in split:
        sco = "i2 0 [60*60*24*7]"
    elif "resonance" in split:
        sco = "i4 0 [60*60*24*7]"

c.ReadScore(sco)
c.Start()
c.SetChannel("loc", File_Dir)
if "please" not in split:
    speak.Speak("Good manners cost nothing, puny human")
    c.Stop()
elif "OK" not in split and "Computer" not in split: 
    speak.Speak("Please use the OK computer command")
    c.Stop()   
elif "set" in split and "cut" in split:
    csCut = float(nums[0])
    print("Cutoff set to {0} hz".format(csCut), csCut, "hz ")
    c.SetChannel("cutoff", csCut)
    cs_Perform()
    
elif "set" in split and "resonance" in split: 
    csRes = float(floats[0])
    print("Resonance set to {0}".format(csRes))
    c.SetChannel("resonance", csRes)
    cs_Perform()
elif "sweep" in split and "cut" in split:
    clow = float(nums[0])
    chigh = float(nums[1])
    ctime = float(nums[2])
    c.SetChannel("lowfreq", clow)
    c.SetChannel("highfreq", chigh)
    c.SetChannel("time", ctime)
    cs_Perform()