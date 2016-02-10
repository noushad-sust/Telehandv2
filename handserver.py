


import Tkinter as tk
import tkMessageBox as box
import Queue
import threading
import time
import ui as gui
from SimpleWebsocketServer import MySimpleWssServer
from abstractrobot import MyRobotHand
from myhwengine import MyHwEngine
'''
Version 2
Wss Server+Arduino+Telehand design.

'''


class MainClass():
    def __init__(self):
        print 'main controller class'
        print 'making websocket server'
        self.hand=MyRobotHand(self.showmsg)

        self.he=MyHwEngine()
        self.regjoints()

        self.root=tk.Tk()
        self.queue = Queue.Queue()
        self.gui = gui.MyUI(self.root, self.queue, self.onexit, self.onuibutton)
        self.showmsg('My WebSocket Secure Server')
        self.showmsg('Python Software and Web Browser Bridge')


        self.running = True
    	self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        self.periodicCall()
        self.root.mainloop()

    def regjoints(self):
        self.he.registerjoint(self.hand.base)
        self.he.registerjoint(self.hand.shoulder)
        self.he.registerjoint(self.hand.bicep)
        self.he.registerjoint(self.hand.elbow)
        self.he.registerjoint(self.hand.handL)
        self.he.registerjoint(self.hand.handR)

    def periodicCall(self):
        self.gui.processIncoming()
        if not self.running:
            import sys
            sys.exit(1)
        else:
            pass
            #print 'running'
        self.root.after(100, self.periodicCall)

    def workerThread1(self):
        self.ws=None
        port=9001
        self.ws=MySimpleWssServer.MyWssServer(self, port)
        self.t = threading.Thread(target=self.dostart)
        self.t.setDaemon(True)
        self.t.start()
        print 'made'
        self.showmsg('WebSocket Daemon Started on: '+str(port)+'\n\n')


    def dostart(self):
        self.ws.run_forever()

    def onuibutton(self, val):
        print 'onbutton=',val

        if val=='Connect Arduino':
            try:
                self.he.start()
                self.he.configjoints()
                print 'configuring joint speed'
                self.he.configjointspeed()
                self.showmsg('connection initiated')
            except:
                box.showerror('Error', 'Can\'t Connect')
        elif val=='Power ON':
            if not self.he.hw.isconnected():
                box.showerror('Warning', 'Arduino Not Connected')
                return

            self.he.pw_on()
        elif val=='Power OFF':
            if not self.he.hw.isconnected():
                box.showerror('Warning', 'Arduino Not Connected')
                return
            self.he.pw_off()
        elif val=='Test':
            #self.hand.base.set(90)
            self.hand.grip_open()
            #call execution cycle now.
            rsp=self.he.updatejoints()
            #self.he.print_response(rsp)
            print 'rsp=',rsp


        elif val=='Test2':
            #self.hand.base.set(120)
            self.hand.grip_close()
            rsp=self.he.updatejoints()
            print 'rsp=',rsp


    def onmsg(self, msg):
        self.showmsg(msg)
        print 'msg=', msg

        try:
            info=msg.split('=')
            id=int(info[1])
            val=int(info[2])
            print 'id=',id,' val=',val
            if id==21:
                self.hand.base.moveto(val)
                rsp=self.he.updatejoints()
                print 'rsp=',rsp
            elif id==22:
                self.hand.shoulder.moveto(val)
                rsp=self.he.updatejoints()
                print 'rsp=',rsp
            elif id==23:
                self.hand.bicep.moveto(val)
                rsp=self.he.updatejoints()
                print 'rsp=',rsp
            elif id==24:
                self.hand.elbow.moveto(val)
                rsp=self.he.updatejoints()
                print 'rsp=',rsp
            elif id==25 and val==1:
                self.hand.grip_close()
                rsp=self.he.updatejoints()
                print 'rsp=',rsp
            elif id==25 and val==0:
                self.hand.grip_open()
                rsp=self.he.updatejoints()
                print 'rsp=',rsp

        except:
            pass


        self.ws.send_msg('echo='+msg+' : '+'success')
    def showmsg(self,msg):
        self.queue.put(msg)
    def onexit(self):
        print 'onexit'
        self.running=False
        #self.ws.close()
        import sys
        sys.exit(0)
        print 'closed'
    '''

    '''
    def handleConnected(self):
        print 'new client'
        self.showmsg('new client')

    def handleClosed(self):
        print 'closed'
        self.showmsg('connection closed')




def main():
    mc=MainClass()


if __name__=='__main__':
    main()
