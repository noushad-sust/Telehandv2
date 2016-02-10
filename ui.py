import Tkinter as tk
import tkMessageBox as box
import Queue

class MyUI():

    def __init__(self, root, queue, onexit, onuibutton):
        self.root =root
        self.onexit=onexit
        self.onuibutton=onuibutton
        self.root.title("MyTelehandServer")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # create a Frame for the Text and Scrollbar
        self.frame = tk.Frame(self.root, width=600, height=400)
        self.frame.pack(fill="both", expand=True)

        self.frame.grid_propagate(False)
        # implement stretchability
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)

        self.queue = queue
        self.initUI()

    def initUI(self):
        label = tk.Label( self.frame, text="Python+Arduino+Websocket+Browser", relief=tk.RAISED )
        label.grid(row=0, column=1, columnspan=2, sticky="news")


        self.v= tk.StringVar()
        # create a Text widget
        self.txt = tk.Text(self.frame, borderwidth=3, relief="sunken" , width=50, height=15 )
        self.txt.config(state='disabled', font=("consolas", 12), undo=True, wrap='word')
        self.txt.grid(row=1, column=1, columnspan=4, padx=2, pady=2, sticky='w')

    # create a Scrollbar and associate it with txt
        scrollb = tk.Scrollbar(self.frame, command=self.txt.yview)
        scrollb.grid(row=1, column=4, sticky='wns')
        #scrollb.pack(side=tk.LEFT)
        self.txt['yscrollcommand'] = scrollb.set


        self.button2=tk.Button(self.frame, text="Connect Arduino" )
        self.button2.grid(row=2, column=0, columnspan=1, sticky='news')
        self.button2.bind("<Button-1>", self.buttoncallback)

        button3=tk.Button(self.frame, text="Power ON" )
        button3.grid(row=2, column=1, columnspan=1, sticky='news')
        button3.bind("<Button-1>", self.buttoncallback)

        button4=tk.Button(self.frame, text="Test" )
        button4.grid(row=2, column=2, columnspan=1, sticky='news')
        button4.bind("<Button-1>", self.buttoncallback)
        button5=tk.Button(self.frame, text="Test2" )
        button5.grid(row=2, column=4, columnspan=1, sticky='news')
        button5.bind("<Button-1>", self.buttoncallback)

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                # As a test, we simply print it
                print msg
                self.v.set("msg="+str(msg) )
                self.showText(str(msg) )

            except Queue.Empty:
                pass
    def buttoncallback(self, event):
        txt=event.widget.cget("text")
        #print 'event=',txt
        if txt=="Power ON":
            event.widget["text"] = "Power OFF"
        elif txt=="Power OFF":
            event.widget["text"] = "Power ON"
        elif txt=='Connect Arduino':
            event.widget.config(state='disabled')
        self.onuibutton(txt)

    def on_closing(self):
        if box.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.onexit()


    def showText(self, txt):
        self.txt.config(state='normal')
        self.txt.insert(tk.END, txt+"\n")
        self.txt.see(tk.END)
        self.txt.config(state='disabled')
