
'''
abstract robot joint.
passive on hardware.
No update on hardware.
hardware execution cycle will take value and update.


'''
class MyAbstractJoint():
    def __init__(self, pin, min=0, max=180, speed=5):
        print 'joint class'
        self.pin=pin

        self.min=min
        self.max=max
        self.default= (self.min+self.max)/2
        self.lastpos=self.default
        self.speed=speed

        self.hasnewval=False

    '''
    call from robot design
    '''
    def moveto(self,pos, commander=None):
        self.hasnewval=True
        self.commander=commander
        ans=True
        if pos<self.min:
            pos=self.min
            ans=False
        elif pos>self.max:
            pos=self.max
            ans=False
        self.newpos=pos
        return ans



    #call from hw engine
    def getlastpos(self):
        return self.lastpos

    #call from hw engine
    def getpin(self):
        return self.pin

    #call from hw engine
    def gotnewvalue(self):
        return self.hasnewval

    #call from hw engine
    def getthenewvalue(self):
        self.hasnewval=False
        return self.newpos

    #hwengine will ask this joint.
    def getnextpossiblevalue(self, i):
        nxtval=self.lastpos
        #print 'ask: new=', self.newpos, 'last=', self.lastpos, 'pin=', self.pin
        if self.newpos > self.lastpos:
            nxtval=self.lastpos+self.speed*i
        else:
            nxtval=self.lastpos-self.speed*i
        ans=True
        if nxtval<self.min:
            nxtval=self.min
            ans=False
        elif nxtval>self.max:
            nxtval=self.max
            ans=False

        return nxtval, ans

    #call from hw engine
    #read value, from arduino.
    def onhwnewval(self, pos):
        #print 'pin=',self.pin, 'updating...'
        self.lastpos=pos

