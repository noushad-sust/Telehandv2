
from abstractjoint import MyAbstractJoint

'''
My Tele Hand designed class
updated: ver2

passive. No access on hardware. HwEngine will call. it.

'''
class MyRobotHand():
    def __init__(self, showonui):
        print 'My Robot Arm design: TeleHand'
        self.showonui=showonui

        self.base=MyAbstractJoint(7, min=40, max=120, speed=40)
        self.shoulder=MyAbstractJoint(6, min=30, max=170, speed=40)
        self.bicep=MyAbstractJoint(5, min=10, max=100, speed=255)
        self.elbow=MyAbstractJoint(4, min=40, max=130, speed=255)

        self.handL=MyAbstractJoint(3, min=10, max=170, speed=255)
        self.handR=MyAbstractJoint(2, min=10, max=170, speed=255)

    def grip_open(self):
        self.handL.moveto(90)
        self.handR.moveto(120)

    def grip_close(self):
        self.handL.moveto(140)
        self.handR.moveto(65)

    def grip2(self):
        print 'grip2'
        posl=150
        posr=65
        hl=self.handL
        hr=self.handR

        ll=posl-hl.lastpos
        lr=posr-hr.lastpos



        return True
