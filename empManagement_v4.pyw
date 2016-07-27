from tkinter import *
from tkinter.messagebox import showinfo
from guiPage_v4 import HRWin


def authenticate():
    passwd = entPassword.get()
    if passwd:
        if passwd.isnumeric():
            if eval(passwd) == 4309:
                root.destroy()
                g = HRWin(Tk())
                center(g.parent)
                g.parent.mainloop() #need to refer to g.parent which is top level window
                                    # but g is just an object of Frame and it can't have
                                    # .mainloo()
                
            else:
                entPassword.delete(0, END)
                showinfo('Try Again', 'Wrong Password! Enter again.')
        else:
            entPassword.delete(0, END)
            showinfo('Wrong Format!', 'Password is a 4 digit number! Enter again.')
    else:
        showinfo('Password', 'Enter your password.')

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))      
   
root = Tk()
root.title('Employee Management')
root.minsize(width = 300, height = 300)

center(root)

labelFont = ('times', 12, 'bold')
entryFont = ('times', 14)

loginFrame = Frame(root, width = 250, height = 200)
loginFrame.propagate(0)
loginFrame.pack(side = BOTTOM)

row1 = Frame(loginFrame)
lblEnter = Label(row1, text = 'Enter Password: ', font = labelFont)
entPassword = Entry(row1, width = 20, font = entryFont)
row1.pack(fill = X)
lblEnter.pack(side = LEFT)
entPassword.focus_set()
entPassword.pack(side = RIGHT)

row2 = Frame(loginFrame)
loginButton = Button(row2, text = 'Login', width = 15, command = authenticate)
Label(row2).pack()
row2.pack()
loginButton.pack()

root.mainloop()
