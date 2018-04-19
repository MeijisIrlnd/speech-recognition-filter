
import csnd6
from Tkinter import *
import speech_recognition as sr 
import sys, os, pyaudio
from pocketsphinx import *



orc = """
sr=44100
ksmps=32
nchnls=2
0dbfs=1

instr 1
kCutoff chnget "cut"
kPortCut port kCutoff, 0.1, i(kCutoff)
aSig vco2 0.5, 80
aFilt moogladder aSig, kPortCut, 0.5
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
        self.config = Decoder.default_config()
        self.config.set_string('-hmm', "C:\Anaconda\Lib\site-packages\pocketsphinx\model\en-us")
        self.config.set_string('-dict', 'C:\Anaconda\Lib\site-packages\pocketsphinx\model\cmudict-en-us.dict')
        self.config.set_string('-keyphrase', 'computer')
        self.config.set_float('-kws_threshold', 1e-1)
        

    def create_widgets(self):
        self.size = 1000
        self.canvas = Canvas(self, height = self.size, width = self.size)
        self.canvas.pack()
        self.runbutton = Button(self.canvas, text = "Start Program", command = self.cs_start)
        self.runbutton.pack()
        

    
    def cs_start(self):
        perfThread.InputMessage("i1 0 3600")
    
    def always_on_sr(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        stream.start_stream()
        decoder = Decoder(self.config)
        decoder.start_utt()
        while True:
            buf = stream.read(1024)
            if buf:
                decoder.process_raw(buf, False, False)
            else:
                break
            if decoder.hyp() != None:
                print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
                print ("Detected keyphrase, restarting search")
                decoder.end_utt()
                self.speech_rec():
                decoder.start_utt()
    
    def speech_rec(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        words = r.recognize_google(audio)
        nums = [int(s) for s in words.split() if s.isdigit()]
        split = words.split()
        print(split)
        if "set" in split and "cut" in split:
            cscut = float(nums[0])
            c.SetChannel("cut", cscut)
        else:
            print("invalid input")
        
    def quit(self):
        self.master.destroy()
        perfThread.Stop()
        perfThread.Join()
    
app = Application(Tk())
app.mainloop()
#python D:\OOP\Speech_Rec_Thread.py