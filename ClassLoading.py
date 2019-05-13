# This module is part of the core Basondole Tools
# This code provides animated loading window for  tasks that take some time to complete
# This module is purely for GUI animation
# AUTHOR: Paul S.I. Basondole

import Tkinter
import ttk
import threading
import time
import Queue

class loading(Tkinter.Frame):

    def __init__(self,frame,parent,pbar=None,words=False):
        Tkinter.Frame.__init__(self,parent,frame)
        ''' disable interaction with the main window when loading '''
        ''' interaction will be restored in the execution function '''
        ''' from the class that called this function '''

        parent.update_idletasks()
        parent.config(cursor="wait")

        self.Loadingwindow = Tkinter.LabelFrame(parent)
        self.Loadingwindow.configure(relief='groove')
        self.Loadingwindow.configure(foreground="black")
        self.Loadingwindow.configure(text='''''')
        self.Loadingwindow.configure(background="#d9d9d9")
        self.Loadingwindow.configure(width=500)


        self.Label1_5 = Tkinter.Label(self.Loadingwindow)
        self.Label1_5.place(relx=0.32, rely=0.346, height=32, width=200
              , bordermode='ignore')
        self.Label1_5.configure(background="#d9d9d9")
        self.Label1_5.configure(disabledforeground="#a3a3a3")
        self.Label1_5.configure(foreground="#000000")
        self.Label1_5.config(text ='Loading... please wait')

        self.pbar1_1 = ttk.Progressbar(self.Loadingwindow, orient="horizontal", length=400, mode="determinate", maximum=20)


        if pbar:
            self.Loadingwindow = Tkinter.LabelFrame(frame)
            if not words:
                self.pbar1_1 = ttk.Progressbar(self.Loadingwindow, orient="horizontal", length=400, mode="determinate", maximum=20)
                self.pbar1_1.pack()
            else:
                self.label_1 = Tkinter.Label(self.Loadingwindow)
                self.label_1.configure(text= words+'...')
                self.label_1.pack()
            self.Loadingwindow.place(relx=pbar[0], rely=pbar[1],relheight=pbar[2], relwidth=pbar[3])
            self.Label1_5.place_forget()
        else:
            self.pbar1_1.place(relx=0.16, rely=0.446)
            self.Loadingwindow.place(relx=0.0, rely=0.09, relheight=1.0, relwidth=0.998)

        self.startbar()
        self.Loadingwindow.tkraise()


    def loopbar(self):
            for num in range(0,20):
                try:
                    item = self.qbar2_1.get(False)
                    if item == 'stop':
                        self.pbar2_1['value']=num
                        self.Loadingwindow.update()
                        continue
                except Queue.Empty: pass
                self.pbar1_1['value']=num
                self.Loadingwindow.update()
                time.sleep(0.02)

    def stop(self,parent):
        parent.config(cursor="")
        self.Loadingwindow.place_forget()
        parent.update()


    def startbar(self):
        self.qbar2_1 = Queue.Queue()
        self.t = threading.Thread(target=self.loopbar())
        self.t.start()


def test():
    parent = Tkinter.Tk()
    parent.geometry("501x336+387+422")
    frame = Tkinter.Frame(parent)
    frame.pack(side="top", fill="both", expand = True)
    d=loading(frame,parent)
    d.stop(parent)
    parent.mainloop()


if __name__ == '__main__':
    test()
