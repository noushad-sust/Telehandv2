from myarduino.hwprotocol2 import HwProtocol
import math

'''
a framework.
115200
'''

class MyHwEngine():
    def __init__(self):
        print 'myhwengine'
        self.abjoints=[]
        self.hw=HwProtocol()

    def pw_on(self):
        self.hw.digital_write(12, HwProtocol.HIGH)
    def pw_off(self):
        self.hw.digital_write(12, HwProtocol.LOW)
    def start(self):
        response=self.hw.connect(com='com6', baud=460800)
        self.print_response(response)
        self.hw.digital_config(12, HwProtocol.OUTPUT)

    def registerjoint(self, abj):
        self.abjoints.append(abj)

    def configjoints(self):
        pvals={}
        if len(self.abjoints)==0:
            return 'NO JOINTS'
        for abj in self.abjoints:
            pvals[abj.pin] =111
        resp=self.hw.servo_config2(pvals)
        return resp
    def configjointspeed(self):
        pvals={}
        if len(self.abjoints)==0:
            return 'NO JOINTS'
        for abj in self.abjoints:
            pvals[abj.pin] =abj.speed
        resp=self.hw.servo_config_speed(pvals)
        return resp

    #sharp move.
    def updatejoints(self):
        rsp=self.readjoints()

        pvals={}
        if len(self.abjoints)==0:
            return 'NO JOINTS'
        for abj in self.abjoints:
            if abj.gotnewvalue()==True:
                pvals[abj.pin] =abj.getthenewvalue()    #making the dictionary.
        resp=self.hw.servo_write2(pvals)
        return resp

    #smoth move.
    def updatejoints2(self):
        rsp=self.readjoints()
        #print 'rsp=',rsp

        pvals={}
        if len(self.abjoints)==0:
            return 'NO JOINTS'
        #find n-iter
        nitr=1
        njoints=[]
        for abj in self.abjoints:
            if abj.gotnewvalue()==True:
                njoints.append(abj)
                pvals[abj.pin] =abj.getthenewvalue()    #making the dictionary.
                nval=abj.getthenewvalue()
                lstval=abj.getlastpos()
                spd=abj.speed
                nstep=math.ceil( math.fabs(nval-lstval)/spd)
                if nstep>nitr:
                    nitr=nstep
                #print 'pin=', abj.pin, 'lst=',lstval, 'nvl=',nval,  'nstep=',nstep

        print 'smooth update: ncylce=', nitr
        #now write value to hardware softly.
        for i in range( int(nitr) ):
            s='d'
            nd={}   #moduler dictionary.
            for joint in njoints:
                nxtval, ans=joint.getnextpossiblevalue(i)
                nd[joint.pin]=nxtval #next value.
                print 'cycle=',i, 'pin=', joint.pin, 'nxtval=',nxtval
                #joint.moveto(nxtval)    #next move.

            #got the dictionary.
            resp, option=self.hw.servo_write2(nd)
            print 'cycle=', i ,'status=', resp

            #update the old newval.

        #resp, option=self.hw.servo_write2(pvals)
        return resp

    def readjoints(self):
        pvals={}
        if len(self.abjoints)==0:
            return 'NO JOINTS'
        for abj in self.abjoints:
            pvals[abj.pin] =111
        resp, option=self.hw.servo_read2(pvals)
        #do update all registered joints.
        print 'option=',option
        if option !='':
            printt='need'
            #sr=2:65,3:150,4:93,5:93,6:93,7:93
            option=option.split('=')[1]
            parts=option.split(',')
            pvals={}
            for part in parts:
                inf=part.split(':')
                pn=inf[0]
                vl=inf[1]
                pvals[pn]=vl    #making the dictionary.
            self.update_registered_joints(pvals)

        return resp

    #local, private call. update all registered joints.
    def update_registered_joints(self, pvals):
        print 'updating registered joints'
        if len(self.abjoints)==0:
            return 'NO JOINTS'
        for abj in self.abjoints:
            for k, v in pvals.items():
                if int(k)==abj.pin:
                    #print 'matched'
                    v=int(v)
                    abj.onhwnewval(v)
                    break
            #one joint updated.
        #all joints updated.

    def print_response(self, response):
        print 'printing response...'
        for line in response:
            print line
        print '.....\n'


