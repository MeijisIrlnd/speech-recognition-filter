from Tkinter import *
import speech_recognition as sr
import csnd6
import re
#import win32com.client as wincl

class Application(Frame):
    def rec_speech(self):
        print("Please Speak Now")
        r = sr.Recognizer()    
        with sr.Microphone() as source:
            audio = r.listen(source)
        words = r.recognize_google(audio)
        self.nums = [int(s) for s in words.split() if s.isdigit()]
        self.floats = re.findall('\d+(\.\d+)?', words)
        self.split = words.split()
        print(self.split)
        self.generate_score()
    def generate_score(self):               
        if "cut" in self.split:
            self.sco = "i1 0 30"
            print(True)
            self.c.ReadScore(self.sco)
        elif "resonance" in self.split:
            self.sco = """i"set_resonance" 0 30"""
            self.c.ReadScore(self.sco)
        
        self.c.Start()
        self.c.Perform()
        self.send_events()
    def send_events(self):
        if "please" not in self.split:
            print("Good manners cost nothing, puny human")
            self.c.Stop()
        elif "OK" not in self.split and "Computer" not in self.split: 
            print("Please use the OK computer command")
            self.c.Stop()   
        elif "set" in self.split and "cut" in self.split:
            csCut = float(self.nums[0])
            OnOff = 1
            print("Cutoff set to {0} hz".format(csCut), csCut, "hz ")
            self.c.SetChannel("cutoff", csCut)
            self.c.SetChannel("OnOff", OnOff)
        elif "set" in self.split and "resonance" in self.split: 
            csRes = float(self.floats[0])
            print("Resonance set to {0}".format(csRes))
            self.c.SetChannel("resonance", csRes)
        self.cs_stop()
    def cs_stop(self):
        self.c.Reset() #ideally on stop button press
    def create_widgets(self):
        frame = Frame(master = None)
        frame.pack()
        recognise = Button(text = "Rec", command = self.rec_speech)
        recognise.pack(side = LEFT)
        QUIT = Button(text = "Exit", fg = "red", command = frame.quit )
        QUIT.pack(side = LEFT)
        STOP = Button(text="Stop", fg = "red", command = self.cs_stop)
        STOP.pack(side = LEFT)
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.orc = """
        sr = 44100
        ksmps = 32
        nchnls = 2
        0dbfs = 1
        instr 1
        kFreq init 0
        kFreq chnget "cutoff"
        SLoc chnget "loc"
        aSig vco2 0.5, 80
        ;aSig, aSig diskin  SLoc
        aFilt moogladder aSig, kFreq, 0.5
        aFilt = aFilt
        outs aFilt, aFilt
        endin
        instr set_resonance
        iRes init 0
        iRes chnget "res"
        SLoc chnget "loc"
        aSig vco2 0.5, 80
        ;aSig, aSig diskin SLoc
        aFilt moogladder aSig, 200, iRes
        outs aFilt, aFilt
        endin     
        instr unused
        prints "running"
        endin
        """
        
        File_Dir = "D:\College\Test.wav"        
        #self.speak = wincl.Dispatch("SAPI.SpVoice")
        self.c = csnd6.Csound()
        self.c.SetOption("-odac 1")
        self.c.SetOption("-m7")
        self.c.CompileOrc(self.orc)
        self.c.ReadScore(self.sco)
        self.c.SetChannel("SLoc", File_Dir)
        
        
        
app = Application(master = Tk())
app.mainloop()
app.destroy()
#python D:\Projects\Python\speech-recognition-filter\Debugging_2.py