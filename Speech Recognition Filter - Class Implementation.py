#OOP Speech Rec
import speech_recognition as sr
import re
import csnd6
import win32com.client as wincl
class Application():
    def speech_rec(self):
        r = sr.Recognizer()
    
        with sr.Microphone() as source:
            audio = r.listen(source)
        words = r.recognize_google(audio)
        self.nums = [int(s) for s in words.split() if s.isdigit()]
        self.floats = re.findall('\d+(\.\d+)?', words)
        self.split = words.split()
        self.generate_score()
    def generate_score(self):        
        
        if "cut" in self.split:
            self.sco = """i"set_cutoff" 0 [60*60*24*7]"""
            self.c.ReadScore(self.sco)
        elif "resonance" in self.split:
            self.sco = """i"set_resonance" 0 [60*60*24*7]"""
            self.c.ReadScore(self.sco)
        self.send_events()
    def send_events(self):
        if "please" not in self.split:
            self.speak.Speak("Good manners cost nothing, puny human")
            self.c.Stop()
        elif "OK" not in self.split and "Computer" not in self.split: 
            self.speak.Speak("Please use the OK computer command")
            self.c.Stop()   
        elif "set" in self.split and "cut" in self.split:
            csCut = float(self.nums[0])
            print("Cutoff set to {0} hz".format(csCut), csCut, "hz ")
            self.c.SetChannel("cutoff", csCut)
        elif "set" in self.split and "resonance" in self.split: 
            csRes = float(self.floats[0])
            print("Resonance set to {0}".format(csRes))
            self.c.SetChannel("resonance", csRes)
        #if button pressed then run speech_rec again
    def __init__(self, master = None): #Constructor
        #Frame.__init__(self, master) #I think this is only for Tkinter
        self.orc = """
        sr = 44100
        ksmps = 32
        nchnls = 2
        0dbfs = 1

        instr set_cutoff
        kFreq init 200
        kFreq chnget "cutoff"
        SLoc chnget "loc"
        print 100
        aSig vco2 0.5, 80
        ;aSig, aSig diskin  SLoc
        aFilt moogladder aSig, kFreq, 0.5
        outs aFilt, aFilt
        endin

        

        instr set_resonance
        iRes init 0.5
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
        self.speak = wincl.Dispatch("SAPI.SpVoice")
        self.c = csnd6.Csound()
        self.c.SetOption("-odac")
        self.c.SetOption("-m7")
        self.c.CompileOrc(self.orc)
        self.c.ReadScore("""i"unused" 0 [60*60*24*7]""")
        self.c.Start()
        self.c.SetChannel("SLoc", File_Dir)
        self.c.Stop() #ideally on stop button press

Run = Application()
Run.mainloop()
        
        
        