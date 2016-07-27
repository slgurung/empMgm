from tkinter import *
from tkinter import ttk

class treeView:
    def __init__(self, container, columnHeading, columnSize, height = 15):
        self.parent = container
        self.columnHeading = columnHeading
        self.columnSize = columnSize
        self.height = height
        self.tree = self.makeTree() #this is Treeview object but an object of treeView()
                                    #is not object of Treeview or any other widget
                                    #compare this with previous version

    def makeTree(self):
        tree = ttk.Treeview(columns = self.columnHeading, show="headings", height = self.height)
        vsb = ttk.Scrollbar(orient = "vertical", command= tree.yview)
        #hsb = ttk.Scrollbar(orient="horizontal", command= tree.xview)
        tree.configure(yscrollcommand = vsb.set) #, xscrollcommand=hsb.set)
        tree.grid(column=0, row=0, sticky='nsew', in_= self.parent)
        vsb.grid(column=1, row=0, sticky='ns', in_= self.parent)
        #hsb.grid(column=0, row=1, sticky='ew', in_= self.container)

        for (i, head) in enumerate(self.columnHeading):
            tree.heading(head, text = head, anchor = W) # text = head.title() -> make 1st letter capital, rest lowercase
            tree.column(head, width = self.columnSize[i], anchor = W)
        '''for i in range(self.height):
            if i%2 == 0:
                tree.insert('', 'end', iid = i, tags = 0)
                tree.tag_configure(0, background = '#e5f7ff')
            else:
                tree.insert('', 'end', iid = i, tags = 1)
                tree.tag_configure(1, background = '#e0ebeb')'''
                
        return tree   #returns Treeview object

if __name__ == '__main__':
    win = Tk()
    container = Frame(win)
    
    tree = treeView(container, ('name', 'add'), (500, 50))
    container.pack()
    win.mainloop()
    
