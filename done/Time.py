#!/usr/bin/env python3
'''Deals with anything with the human concept of time and dates'''

from time import *
from datetime import datetime

class Time:
    def __init__(self, *time):
        """Instance of time can do many Timely things.
        
        Keeps track of total seconds from midnite to time.
        
        Initialization:
            
            All of these are equavilent and will initialize with 8 o'clock AM
            
            Time(8,0,0) - set hours, minutes, seconds
            Time(8,0) - set hours, minutes
            Time(8) - set hours
            Time('8') - set hours from string
            Time('8:0') - set hours, minutes from string
            Time('8:0:0') - set hours, minutes, seconds from string
        
        If initialization fails will return a Time() instance with time of creation
        """
        try:
            if len(time)==1:
                if type(time[0])==str: new = time[0].split(":")
                else: new = [self.run(time[0],0),0,0]
            elif len(time)>1: new = [self.run(i,0) for i in time[:3]]
            else: raise Exception()
        except:
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
    def totalSc(self):
        """Calculate and return the total amount of seconds from midnite to time"""
        return 60*(60*self.hr+self.mn)+self.sc
    def hrHandDeg(self):
        """Calculate and return angle between the 12 and position of the hour hand"""
        return (60*(60*self.hr+self.mn)+self.sc)/120%360
    def mnHandDeg(self):
        """Calculate and return angle between the 12 and position of the minute hand"""
        return (60*self.mn+self.sc)/10%360
    def scHandDeg(self):
        """Calculate and return angle between the 12 and position of the second hand"""
        return self.sc*6%360
    #Some setting functions
    def fromS(self,secs):
        """Set the time according to how many seconds from midnite the time should be"""
        self.hr,self.mn,self.sc = int((secs/120%360))//30,int((secs/10%360))//6,(secs*6%360)/6
        if abs(self.sc%1) < 1e-9: self.sc=int(self.sc)+.0
        return self
    def hrFromD(self,deg):
        """Set the hour hand of time to where it should be according to the angle given in degrees"""
        self.hr=deg//30
    def mnFromD(self,deg):
        """Set the minute hand of time to where it should be according to the angle given in degrees"""
        self.mn=deg//6
    def scFromD(self,deg):
        """Set the second hand of time to where it should be according to the angle given in degrees"""
        self.sc=deg/6
    def setHr(self, num):
        """Set the hours of time"""
        new = Time(num,self.mn,self.sc)
        self.hr,self.mn,self.sc = new.hr,new.mn,new.sc
    def setMn(self, num):
        """Set the minutes of time"""
        new = Time(self.hr,num,self.sc)
        self.hr,self.mn,self.sc = new.hr,new.mn,new.sc
    def setSc(self, num):
        """Set the seconds of time"""
        new = Time(self.hr,self.mn,num)
        self.hr,self.mn,self.sc = new.hr,new.mn,new.sc
    #Some math operations for time
    def __add__(self, new): return Time(self.hr+new.hr,self.mn+new.mn,self.sc+new.sc)
    def __sub__(self, new): return Time(self.hr-new.hr,self.mn-new.mn,self.sc-new.sc)
    def __mul__(self, new): return Time(0).fromS(self.totalSc()*self.run(new,1))
    def __truediv__(self,new): return Time(0).fromS(self.totalSc()/self.run(new,1))
    def __floordiv__(self,new): return Time(0).fromS(self.totalSc()//self.run(new,1))
    def __mod__(self,new): return Time(0).fromS(self.totalSc()%self.run(new,self.totalSc()+1))
    def __round__(self,n): return Time(self.hr,self.mn,round(self.sc,n))
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
    def __repr__(self): return '{:0>2}:{:0>2}:{:0>2}'.format(self.hr,self.mn,self.sc)
    def __str__(self): return self.__repr__()
    def run(self,num,default=1):
        """Convert parameter sent into the total amount of seconds.
        
        Can accept int, float, and Time. Anything else and default is returned"""
        if type(num)==type(self): return num.totalSc()
        if type(num) in [int, float]: return num
        return default

def bisectHrMnHands(hr,mn):
    """Calculate the time at which the second hand will bisect the hour and minute hands"""
    h = int(hr) 
    m = int(mn)
    sDegMin = (60*h+m)/2
    sDegMax = 6*m
    while 1:
        sDeg = (sDegMin+sDegMax)/2
        hDeg = (60*h+m)/2 + sDeg/6/120
        mDeg = 6*m + sDeg/60
        if   2*sDeg== hDeg+mDeg : return '{:0>2}:{:0>2}:{:0>2}'.format(h,m,(sDeg%360)/6)
        elif 2*sDeg < hDeg+mDeg : sDegMin = sDeg
        else                    : sDegMax = sDeg

def DayOfTheWeek(month,date,year):
    """"Calculate the Day of the Week according to month, day, year given."""
    if type(month)==str: month = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'].index(month.lower()[:3])+1
    return ['Thrusday','Friday','Saturday','Sunday','Monday','Tuesday','Wednesday'][int((23*month//9+date+year+(year-(1-abs(month-2.5)/(month-2.5))//2)//4-(year-(1-abs(month-2.5)/(month-2.5))//2)//100+(year-(1-abs(month-2.5)/(month-2.5))//2)//400)-abs(month-2.5)/(month-2.5)-1)%7]

from contextlib import contextmanager
@contextmanager
def timer(msg):
    """Give time taken by the block within context.
    
    Usage:
    
        with timer('<Message>'):
            <block>
    """
    start = time()
    yield
    end = time()
    print("%s: %.02fms" % (msg, (end-start)*1000))

def stopwatch(n=10):
    """Give time SINCE call for {n} Enter Key presses."""
    a = datetime.now()
    for i in range(n):
        input()
        print(datetime.now() - a)
countUp = stopwatch
def countBetween(n=10):
    """Give time BETWEEN key presses for {n*2} Enter Key presses."""
    for i in range(n):
        input("[Start]")
        a = datetime.now()
        input("Counting...")
        print(datetime.now()-a)
def countdown(n=10,count=1):
    """Show a countdown on the Terminal starting at {n} counting down by {count}"""
    a = Time()+Time(0,0,n*count)
    while a>Time():
        print(round((a-Time())/count,0),end="\r")
        sleep(count)

def QuickThread(f):
    from threading import Thread
    t = Thread(target = f, daemon=True)
    t.start()
    return t