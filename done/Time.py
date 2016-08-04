Info ='''---Time---
Deals with anything with the human concept of time and dates

Time(timeStr) - Object to deal with the object of time
bisectHrMnHands(hr,mn,sc) - bisect the hr & mn hands using sc hand
DayOfTheWeek(month,date,year) - Calculates the day of the week
countdown(keyTilQuit=10) - shows amount of time passed on keypress
stopwatch(totalIters=10,secsTilNext=1) - prints time left
timer(str) - Contextual timer called using a with statement
from time import time
'''
def showInfo():
    from done.String import smartPrint
    smartPrint(Info)

class Time:
    def __init__(self, *time):
        "Time(8,0,0)=Time(8,0)=Time(8)=Time('8')=Time('8:0')=Time('8:0:0')"
        try:
            if len(time)==1:
                if type(time[0])==str: new = time[0].split(":")
                else: new = [self.run(time[0],0),0,0]
            elif len(time)>1: new = [self.run(i,0) for i in time[:3]]
            else: 1/0
        except:
            from datetime import datetime
            a=datetime.now()
            new=[a.hour,a.minute,a.second+a.microsecond/1e6]
        while len(new)<3: new=list(new)+[0]
        self.sc=float(new[2])+(float(new[1])+float(new[0])*60)*60
        self.mn=int(self.sc//60) #Get some minutes from it
        self.hr=int(self.mn//60%12) #Get hours from the minutes gotten
        self.mn=int(self.mn%60) #Reduce minutes
        self.sc=round(self.sc%60,9) #Reduce seconds
        #That's the best way I thought of at the moment
    #Some numbers associated with the time
    def totalSc(self): return 60*(60*self.hr+self.mn)+self.sc
    def hrHandDeg(self): return (60*(60*self.hr+self.mn)+self.sc)/120%360
    def mnHandDeg(self): return (60*self.mn+self.sc)/10%360
    def scHandDeg(self): return self.sc*6%360
    #Some setting functions
    def fromS(self,secs):
        self.hr,self.mn,self.sc = int((secs/120%360))//30,int((secs/10%360))//6,(secs*6%360)/6
        if abs(self.sc%1) < 1e-9: self.sc=int(self.sc)+.0
        return self
    def hrFromD(self,deg): self.hr=deg//30
    def mnFromD(self,deg): self.mn=deg//6
    def scFromD(self,deg): self.sc=deg/6
    def setHr(self, num):
        new = Time(num,self.mn,self.sc)
        self.hr,self.mn,self.sc = new.hr,new.mn,new.sc
    def setMn(self, num):
        new = Time(self.hr,num,self.sc)
        self.hr,self.mn,self.sc = new.hr,new.mn,new.sc
    def setSc(self, num):
        new = Time(self.hr,self.mn,num)
        self.hr,self.mn,self.sc = new.hr,new.mn,new.sc
    #Some math operations for time
    def __add__(self, new): return Time(self.hr+new.hr,self.mn+new.mn,self.sc+new.sc)
    def __sub__(self, new): return Time(self.hr-new.hr,self.mn-new.mn,self.sc-new.sc)
    def __mul__(self, new): return Time(0).fromS(self.totalSc()*self.run(new,1))
    def __truediv__(self,new): return Time(0).fromS(self.totalSc()/self.run(new,1))
    def __floordiv__(self,new): return Time(0).fromS(self.totalSc()//self.run(new,1))
    def __mod__(self,new): return Time(0).fromS(self.totalSc()%self.run(new,self.totalSc()+1))
    #Comparisons
    def __lt__(self,new):
        if type(new)==type(self): return self.totalSc()<new.totalSc()
        try: return self.totalSc()<new
        except: return True
    def __eq__(self,new):
        if type(new)==type(self): return self.totalSc()==new.totalSc()
        return False
    def __ne__(self,new): return not self==new
    def __le__(self,new): return self<new or self==new
    def __gt__(self,new): return not self<=new
    def __ge__(self,new): return not self<new
    #Show the time in a cool way
    def __repr__(self): return '{:0>2}:{:0>2}:{:0>2}'.format(self.hr if self.hr!=0 else 0,self.mn,self.sc)
    def __str__(self): return self.__repr__()
    def run(self,num,default):
        if type(num)==type(self): return num.totalSc()
        if type(num) in [int, float]: return num
        return default

def bisectHrMnHands(hr,mn,sc):
    "_(12,30,00) = 12:30:16.39"
    def xpct(hr,mn,sc):
        ans1=((30*hr+6.5*mn+13*sc/120)%360)/2
        ans2=ans1+180
        if abs(sc*6%360-ans1)>abs(sc*6%360-ans2): return ans2
        return ans1
    while round(xpct(hr,mn,sc),9)!=round(sc*6%360,9):
        while xpct(hr,mn,sc)<sc*6%360: sc-=(sc*6%360-xpct(hr,mn,sc))/6
        while xpct(hr,mn,sc)>sc*6%360: sc+=(xpct(hr,mn,sc)-sc*6%360)/6
    secs=60*(60*hr+mn)+sc
    hr=int((secs/120%360)//30)
    mn=int((secs/10%360)//6)
    sc=(secs*6%360)/6
    out=''
    if hr==0: hr=12
    if hr<10: out+='0'
    out+=str(hr)+' : '
    if mn<10: out+='0'
    out+=str(mn)+' : '
    if sc<10: out+='0'
    return out+str(sc)

def DayOfTheWeek(month,date,year):
    "_(12, 25, 1995) = 'Sunday'"
    if type(month)==str: month = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'].index(month.lower()[:3])+1
    return ['Thrusday','Friday','Saturday','Sunday','Monday','Tuesday','Wednesday'][int((23*month//9+date+year+(year-(1-abs(month-2.5)/(month-2.5))//2)//4-(year-(1-abs(month-2.5)/(month-2.5))//2)//100+(year-(1-abs(month-2.5)/(month-2.5))//2)//400)-abs(month-2.5)/(month-2.5)-1)%7]

def stopwatch(n=10):
    from datetime import datetime
    from os import system
    a = datetime.now()
    for i in range(n):
        system('read -s -n 1')
        print(datetime.now() - a)
def countdown(n=10,count=1):
    from os import system
    from time import sleep
    a = Time()+Time(0,0,n*count)
    while a>Time():
        print(a-Time(),end="\r")
        sleep(count)
from contextlib import contextmanager
from time import time
@contextmanager
def timer(msg):
    "with timer('Message'): #do something"
    start = time()
    yield
    end = time()
    print("%s: %.02fms" % (msg, (end-start)*1000))