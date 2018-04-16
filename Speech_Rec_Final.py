
import csnd6
from Tkinter import *
import speech_recognition as sr 
import re

orc = """
sr=44100
ksmps=32
nchnls=2
0dbfs=1

instr 1
kCutoff chnget "cut"
aSig vco2 0.5, 80
aFilt moogladder aSig, kCutoff, 0.5
outs aFilt, aFilt
endin"""
c = csnd6.Csound()
c.SetOption("-odac")
c.SetOption("-m7")
c.CompileOrc(orc)
c.Start()
perfThread = csnd6.CsoundPerformanceThread(c)
perfThread.Play()

class Application(Frame):
    def __init__(self, master = None):
        master.title = ("Speech Recognition Filter")
        c.SetChannel("cut", 20000.0) #initialise 
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

    def create_widgets(self):
        self.size = 1000
        self.canvas = Canvas(self, height = self.size, width = self.size)
        self.canvas.pack()
        self.recbutton = Button(self.canvas, text = "Speak", command = self.speech_rec)
        self.recbutton.pack()
        self.runbutton = Button(self.canvas, text = "Start Program", command = self.cs_start)
        self.runbutton.pack()
        

    def speech_rec(self):
        self.r = sr.Recognizer()
        with sr.Microphone() as source:
            self.audio = self.r.listen(source)
        words = self.r.recognize_google(self.audio)
        self.nums = [int(s) for s in words.split if s.isdigit()]
        self.split = words.split()
        print(self.split)
        if "set" in self.split and "cut" in self.split:
            self.cscut = float(self.nums[0])
            c.SetChannel("cut", self.cscut)
        else:
            print("invalid input")
    def cs_start(self):
        perfThread.InputMessage("i1 0 3600")
    def quit(self):
        self.master.destroy()
        perfThread.Stop()
        perfThread.Join()

app = Application(Tk())
app.mainloop()
#python D:\OOP\Speech_Rec_Final.py