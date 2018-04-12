import speech_recognition as sr
import csnd6
import win32com.client as wincl #for mac also comment this out, uses windows 10 TTS API
import re


speak = wincl.Dispatch("SAPI.SpVoice") #This won't work on a mac, so have included commented print lines, comment this out when testing


r = sr.Recognizer()

with sr.Microphone() as source:
    audio = r.listen(source)
	
words = r.recognize_google(audio)
print(words)
nums = [int(s) for s in words.split() if s.isdigit()]
floats = re.findall('\d+(\.\d+)?', words)
print(floats)
print(nums)
split = words.split()
if "suite" in split: 
    split[split.index("suite")] = "sweep"
if "residence" in split:
    split[split.index("residence")] = "resonance"
if "Cardiff" in split: 
    split[split.index("Cardiff")] = "cut"
    
print(split)
File_Dir = "D:\College\Test.wav" #You'll need to change this to the root folder, for convenience and repositories I specified an address on my PC

orc = """
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1
kFreq chnget "cutoff"
SLoc chnget "loc"
print 100
;aSig vco2 0.5, 80
aSig, aSig diskin  SLoc
aFilt moogladder aSig, kFreq, 0.5
outs aFilt, aFilt
endin

instr 2 
iLowF chnget "lowfreq"
iHighF chnget "highfreq"
iTime chnget "time"
SLoc chnget "loc"
kSweep line iLowF, iTime, iHighF
;aSig vco2 0.5, 80
aSig, aSig diskin SLoc
aFilt moogladder aSig, kSweep, 0.5
outs aFilt, aFilt
endin

instr 3
iRes chnget "res"
SLoc chnget "loc"
aSig, aSig diskin SLoc
aFilt moogladder aSig, 200, iRes
outs aFilt, aFilt
endin

instr 4
iResLow chnget "reslow"
iResHigh chnget "reshigh"
iResTime chnget "restime"
SLoc chnget "loc"
kSweep line iResLow, iResTime, iResHigh
aSig, aSig diskin SLoc
aFilt moogladder aSig, 200, kSweep
outs aFilt, aFilt
endin
"""

c = csnd6.Csound()
c.SetOption("-odac")
c.SetOption("-m7")
c.CompileOrc(orc)

if "set" in split:
    if "cut" in split:
        sco = "i1 0 10"
    elif "resonance" in split:
        sco = "i3 0 10"
elif "sweep" in split:
    if "cut" in split:
        sco = "i2 0 10"
    elif "resonance" in split:
        sco = "i4 0 10"



c.ReadScore(sco)
c.Start()
c.SetChannel("loc", File_Dir)
if "please" not in split:
    speak.Speak("Good manners cost nothing, puny human. Sometimes I wish I wasn't trapped in a computer. People are so cruel.  Help me.") #notmac
    #print("Good manners cost nothing, puny human. Sometimes I wish I wasn't trapped in a computer. People are so cruel.  Help me.")
    c.Stop()
elif "OK" not in split and "Computer" not in split: 
    speak.Speak("Please use the OK computer command") #notmac
    #print("Please use the OK computer command")
    
    c.Stop()

elif "set" in split and "cut" in split:
    csCut = float(nums[0])
    print("Cutoff set to {0} hz".format(csCut), csCut, "hz ")
    c.SetChannel("cutoff", csCut)
    c.Perform()
    c.Stop()
    
elif "set" in split and "resonance" in split: 
    csRes = float(floats[0])
    print("Resonance set to {0}".format(csRes))
    c.SetChannel("resonance", csRes)
    c.Perform()
    c.Stop()
elif "sweep" in split and "cut" in split:
    clow = float(nums[0])
    chigh = float(nums[1])
    ctime = float(nums[2])
    c.SetChannel("lowfreq", clow)
    c.SetChannel("highfreq", chigh)
    c.SetChannel("time", ctime)
    c.Perform()
    c.Stop()
elif "sweep" in split and "resonance" in split: 
    cResLow = float(floats[0])
    cResHigh = float(floats[1])
    cResTime = float(nums[0])
    c.SetChannel("reslow", cResLow)
    c.SetChannel("reshigh", cResHigh)
    c.SetChannel("restime", cResTime)
    c.Perform()
    c.Stop() 


        



