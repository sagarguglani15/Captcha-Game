import os,random
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image

root=Tk()
root.geometry('1000x500')
root.title('Captcha Game')

class Captcha(Canvas):
    def __init__(self, **kw):
        super().__init__(width=1100,height=600,highlightthickness=0,**kw)
        self.k=os.listdir('DataSet')
        print(self.k)
        self.score=0
        self.min=1
        self.sec=30
        self.load_assets()
        self.after(200,self.highlight_heading)
        self.show_instructions()

    def load_assets(self):
        self.bg = Image.open('bg.jpeg')
        self.bgtk = ImageTk.PhotoImage(self.bg)
        self.create_image(100, 0, image=self.bgtk)
        self.create_text(300, 50, text='Welcome to the Captcha Game !', fill='yellow', tag='head',
                         font='Abc 20 bold underline italic')

    def highlight_heading(self):
        curr_head_color=self.itemcget(self.find_withtag('head'),'fill')
        if(curr_head_color == 'yellow'):
            self.itemconfigure(self.find_withtag('head'),fill='light green')
        elif(curr_head_color == 'light green'):
            self.itemconfigure(self.find_withtag('head'), fill='yellow')
        self.after(300,self.highlight_heading)

    def end_inst(self,event):
        self.delete(self.find_withtag('it2'), self.find_withtag('it1'), self.find_withtag('it3'), self.find_withtag('it4'),
                    self.find_withtag('it5'), self.find_withtag('it6'), self.find_withtag('it7'), self.find_withtag('btrok'),
                    self.find_withtag('bttok'))
        self.start_game()

    def start_game(self):
        self.create_text(700, 50, text=('0' + str(self.min) + ':' + str(self.sec)), fill='white',
                         font='Abc 15 bold', tag='time')
        self.create_text(700, 100, text=f'Score: {self.score}', fill='white', font='Abc 15 bold', tag='score')
        self.timer()
        self.create_text(430, 320, tag='result', font='Abc 20 bold italic')
        self.load_image()

    def load_image(self):
        self.s=random.choice(self.k)

        self.image=Image.open('DataSet/'+self.s)
        self.imagetk=ImageTk.PhotoImage(self.image)
        self.create_image(400, 150, image=self.imagetk,tag='captcha_image')

        self.e1=Entry(root,bd=1,fg='midnight blue', bg='white', font='abc 15')
        self.e1.focus_set()
        self.create_window(400,250,window=self.e1,tag='captcha_entry')

        self.bind_all('<Key>',self.on_enter_press)

    def on_enter_press(self,e):
        entered=e.keysym
        if(entered == 'Return' or entered == 'KP_Enter'):
            if (self.e1.get() == self.s[:-4]):
                self.score+=1
                self.itemconfigure(self.find_withtag('result'),fill='light green',text='Correct!')
            else:
                self.itemconfigure(self.find_withtag('result'), fill='red', text='Wrong Answer!')
            self.delete(self.find_withtag('captcha_image'),self.find_withtag('captcha_entry'))
            self.itemconfigure(self.find_withtag('score'),text=f'Score: {self.score}')
            self.load_image()


    def timer(self):
        self.delete(self.find_withtag('time'))
        self.sec-=1
        if(self.sec<10):
            self.create_text(700,50,text=( '0' + str(self.min) + ':0' + str(self.sec) ) ,fill='white',
                         font='Abc 15 bold', tag='time')
        else:
            self.create_text(700, 50, text=('0' + str(self.min) + ':' + str(self.sec)), fill='white',
                             font='Abc 15 bold', tag='time')

        if(self.sec == 0):
            if(self.min == 1):
                self.min-=1
                self.sec=60
            elif(self.min == 0):
                messagebox.showwarning('Time Up !',f'Your score: {self.score}')
                return
        self.after(1000,self.timer)


    def show_instructions(self):
        self.create_text(100,100,text='Instructions: ',fill='white',font='Abc 15 bold',tag='it1')
        self.create_text(500, 150, text='1. You will be shown a random image containing a captcha ( case sensitive ).',fill='red',
                         font='Abc 15 bold',tag='it2')
        self.create_text(395, 200, text='2. You have to enter the captcha in the text box provided.', fill='cyan',
                         font='Abc 15 bold',tag='it3')
        self.create_text(392, 250, text='3. Once you press enter, the captcha will be checked and \n'
                                        '   your score will be updated according to your response.', fill='red',
                         font='Abc 15 bold',tag='it4')
        self.create_text(417, 300, text='4. The game goes for 1:30 minutes, Score as much as you can.', fill='cyan',
                         font='Abc 15 bold',tag='it5')
        self.create_text(427, 350, text='5. The timer will be shown on the top right corner of the screen.', fill='red',
                         font='Abc 15 bold',tag='it6')
        self.create_text(400, 430, text='Best of Luck !', fill='white',
                         font='Abc 15 bold',tag='it7')
        self.create_rectangle(520, 420, 580, 450, fill="yellow", outline="red",tag='btrok')
        self.create_text(550, 435, text="OK",fill='green',font='Abc 15 bold',tag='bttok')
        self.tag_bind(self.find_withtag('btrok'), "<Button-1>", self.end_inst)
        self.tag_bind(self.find_withtag('bttok'), "<Button-1>", self.end_inst)

captcha=Captcha()
captcha.pack()

root.mainloop()