from tkinter import *
#from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import showinfo
from tkinter.messagebox import askquestion
#import os, sys
#import tempfile
#import win32api
import win32print
import win32ui

from decimal import Decimal
import shelve
import calendar

from treeView_v1 import treeView
from employee import Employee
#from calenderGui import MonthlyCalender
from payPeriod_v1 import PayPeriod
from weeklyTime_v1 import WeeklyTime
#from settingGui import SettingGui

##### Most of these global variables should be in setting files
fieldName = ('Name', 'Street', 'City', 'State', 'ZIP', 'Phone', 'Pay Rate', 'Hire Date')
fieldSize = (60, 200, 330, 170, 100, 80, 100, 70, 110)
#timeSheetHeading = ''
#timeSheetHeading = ('Id', 'Name', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Total')
timeSheetHeadingSize = (45, 135, 140, 140, 140, 140,140,140,140, 62)
payrollHeading =('Id', 'Name', 'Total Hours', 'Regular Hour', 'Over Time', 'Regular Rate', 'OT Rate','Total Pay', 'Tips')
payrollHeadingSize = (60, 200, 80, 80, 80, 80, 80, 100, 80)


shelveDB = 'empShelve' #maybe create emp list for each week payroll for future update and lookup
employeeDB = shelve.open( 'empData/' + shelveDB)
payrollDB = 'timeDB' # prefix of timesheet & payroll database

#daysName = ('sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat')
labelFont = ('times', 14,)
entryFont = ('times', 14)
buttonFont = ('times', 11, 'bold')


'''Note about version
guiPage_v3.py is almost same as _v2 but without 
the old codes. I need to see old codes with modified
check _v2 code.
'''

class HRWin(Frame):
    def __init__(self, parent = None):
        self.parent = parent
        self.parent.title('Employee Time & Payroll Management System:')
        self.parent.minsize(width = 1260, height = 800)
        self.parent.resizable(width = FALSE, height = FALSE)
        Frame.__init__(self, parent)
        
        settingDB = shelve.open('setting/' + 'settingFile')
        self.firstDay = settingDB['firstDay']
        self.weekDayOrder = settingDB['weekDayOrder']
        #####need to call this before calling PayPeriod()#############
        calendar.setfirstweekday(self.firstDay) #6 is sunday, can do like,calendar.setfirstweekday(calendar.SUNDAY)
        
        settingDB.close()        
        
        topMenu = Menu(self.parent)
        self.parent.config(menu = topMenu)

        fileMenu = Menu(topMenu, tearoff = 0)
        fileMenu.add_command(label = 'Print')
        fileMenu.add_command(label = 'Exit', command = self.quitProgram)
        topMenu.add_cascade(label = 'File', menu = fileMenu)
        
        payrollMenu = Menu(topMenu, tearoff = 0)
        payrollMenu.add_command(label = 'Enter Time', command = self.addTimeGui)
        payrollMenu.add_command(label = 'Update Time', command = self.updateTimeGui)
        payrollMenu.add_separator()
        payrollMenu.add_command(label = 'View Time',  command = self.viewTime)
        topMenu.add_cascade(label = 'Time', menu = payrollMenu)
        
        
        employeeMenu = Menu(topMenu, tearoff = 0)
        employeeMenu.add_command(label = 'Add New', command = self.addEmpGui)
        employeeMenu.add_command(label = 'Update', command = self.updateEmpGui)
        employeeMenu.add_separator()
        employeeMenu.add_command(label = 'Payroll', command = self.payrollGui)
        topMenu.add_cascade(label = 'Employee', menu = employeeMenu)
        
        
        optionsMenu = Menu(topMenu, tearoff = 0)
        optionsMenu.add_command(label = 'Settings')
        topMenu.add_cascade(label = 'Options', menu = optionsMenu)

        helpMenu = Menu(topMenu, tearoff = 0)
        helpMenu.add_command(label = 'About eManagement System')
        topMenu.add_cascade(label = 'Help', menu = helpMenu)
        
        self.fetchedEmp = ''
        self.entries = {}
        self.mode = ''
        self.timeSheetDB = ''
       
        self.timeSheetHeading = ['Id', 'Name']  + self.weekDayOrder + ['Total']
        #print('week day order: ', self.weekDayOrder)
     
    def empDataDisplayGui(self):
        self.container1 = Frame(self.parent,width = 1250, height = 40)
        self.container1.propagate(0)
        self.container1.pack()
        
        Label(self.container1,text = 'eManagement System', font = ('times', 16, 'bold')).pack()
                       
        self.container2 = Frame(self.parent, width = 1250, height = 353, bd = 2, relief = RIDGE)
        self.container2.propagate(0)
        self.container2.pack()
        viewFrame = Frame(self.container2, width = 1250, height = 352, bd = 2, relief = RIDGE )
        viewFrame.propagate(0)
        viewFrame.pack(anchor = W)

        columnHeading = ('Id',) + fieldName
        self.tView = treeView(viewFrame, columnHeading, fieldSize, 16)
        self.tView.tree.bind('<Double-1>', self.fetchClick)
        self.loadEmpData() # Loads emp data on tView with row colors
        
        
    def empDataEntryGui(self):
        
        self.container3 = Frame(self.parent, width = 1250, height = 300)
        self.container3.propagate(0)
        self.container3.pack()
        
        entryFrame = Frame(self.container3, width = 400, height = 300, bd = 2, relief = RIDGE)
        entryFrame.propagate(0) # works if use pack() inside but not grid()
        entryFrame.pack(side = LEFT)
    
                    
        row = Frame(entryFrame, width = 350, height = 35)
        row.propagate(0)
        row.pack(side = TOP, anchor = W)
        Label(row, text = 'Employee Information Entry Form:', font = ('times',12,'bold')).pack()
        

        idRow = Frame(entryFrame)
        idLabel = Label(idRow, text = 'ID', font = labelFont, width = 8, anchor = E)
        self.idValue = Label(idRow, font = entryFont, width = 6, bd = 2, relief = RIDGE)
        idLabel.pack(side = LEFT)
        self.idValue.pack(side = LEFT)
        idRow.pack(side = TOP, anchor = W, fill = X )
       
        
        entryBoxSize = (32, 32, 20, 15, 12, 12, 12, 12)
        for (i, label) in enumerate(fieldName):
            row = Frame(entryFrame)
            labelName = Label(row, text=label, font = labelFont, width = 8, anchor = E)
            entryData = Entry(row, font = entryFont, width = entryBoxSize[i])
            entryData.bind('<Button-1>', self.entrySelection)
            row.pack(side = TOP, anchor = W, fill = X )
            labelName.pack(side = LEFT)
            entryData.pack(side = LEFT)
            self.entries[label] = entryData
        self.entryFrame = entryFrame
        
        self.buttonFrame = Frame(self.container3, width = 850, height = 300, bd = 2, relief = RIDGE)
        self.buttonFrame.propagate(0)
        self.buttonFrame.pack(side = LEFT)

        row1 = Frame(self.buttonFrame)

        row1.pack(side = BOTTOM, anchor = W, fill = X)

        clearButton = Button(row1, text = 'Clear',font = buttonFont, width = 13, height = 3,
                             command = self.clearForm)        
        closeButton = Button(row1, text = 'Close', font = buttonFont, height = 3, width = 13,
                            command = self.closeGui)
        clearButton.pack(side =LEFT , anchor = S)      
        closeButton.pack(side = LEFT, anchor = S)

        self.modeFrame = Frame(self.buttonFrame) #may not need to creat ??????????????
        self.modeFrame.pack(side = TOP, anchor = W)
        
    def timeDisplayGui(self):
        self.container1 = Frame(self.parent,width = 1250, height = 40)
        self.container1.propagate(0)
        self.container1.pack()
        
        Label(self.container1,text = 'eManagement System', font = ('times', 16, 'bold')).pack()
                       
        self.container2 = Frame(self.parent, width = 1250, height = 353, bd = 2, relief = RIDGE)
        self.container2.propagate(0)
        self.container2.pack()
        
        viewFrame = Frame(self.container2, width = 1250, height = 352,  bd = 2, relief = RIDGE)
        viewFrame.propagate(0)
        viewFrame.pack(anchor = W)
        
        self.timeSheetView = treeView(viewFrame, self.timeSheetHeading, timeSheetHeadingSize, 16)
        self.timeSheetView.tree.bind('<Double-1>', self.fetchClick)
        
        
    def timeEntryGui(self, ppObj):
        self.container3 = Frame(self.parent, width = 1250, height = 360)
        self.container3.propagate(0)
        self.container3.pack()

        ##########
        payrollEntryFrame = Frame(self.container3, width = 450, height = 345, bd = 2, relief = RIDGE)
        payrollEntryFrame.propagate(0)
        payrollEntryFrame.pack(side = LEFT, anchor = N)
        Label(payrollEntryFrame).pack()
        
        timeRow1 = Frame(payrollEntryFrame)
        payLbl = Label(timeRow1, text = 'Pay Period: ', width= 12, font = labelFont,anchor = E)
        payPeriodLbl = Label(timeRow1, text = ppObj.payPeriod, font = labelFont, fg = 'red')
        payLbl.pack(side = LEFT)
        payPeriodLbl.pack(side = LEFT)
        timeRow1.pack(anchor = W)
        
        timeRow2 = Frame(payrollEntryFrame)
        empIDLbl = Label(timeRow2, text = 'ID: ', width = 12, font = labelFont, anchor = E )
        self.empIDVal = Label(timeRow2, font = labelFont, fg = 'blue')
        empIDLbl.pack(side = LEFT)
        self.empIDVal.pack(side = LEFT)
        timeRow2.pack(anchor = W)

        timeRow3 = Frame(payrollEntryFrame)
        empNameLbl = Label(timeRow3, text = 'Name: ', width = 12, font = labelFont, anchor = E )
        self.empNameVal = Label(timeRow3, font = labelFont, fg = 'blue')
        empNameLbl.pack(side = LEFT)
        self.empNameVal.pack(side = LEFT)
        timeRow3.pack(anchor = W)


        timeRow4 = Frame(payrollEntryFrame,width = 450, height = 240, bd = 2, relief = RIDGE)
        timeRow4.propagate(0)    #make Frame fixed size
        timeRow4.pack(fill = X)
        titleRow = Frame(timeRow4)
        nameLbl = Label(titleRow, width = 12, font = labelFont)
        nameLbl.pack(side = LEFT)
        timeInLbl = Label(titleRow, width = 6, font = labelFont, text = 'Time In')
        timeInLbl.pack(side = LEFT)
        nameLbl = Label(titleRow, width = 8, font = labelFont)
        timeOutLbl = Label(titleRow, width = 8, font = labelFont, text = 'Time Out', anchor = W)
        titleRow.pack(anchor = W, fill = X)
        nameLbl.pack(side = LEFT)
        timeOutLbl.pack(side = LEFT)

        inOutMatrix = [[0]*2 for i in range(7)]
        self.AmPm = [[0]*2 for i in range(7)]
        
        for i in range(7):
            self.AmPm[i][0] = IntVar()
            self.AmPm[i][1] = IntVar()
           
            row = Frame(timeRow4)
            dayTxt = self.weekDayOrder[i] + ', ' + str(ppObj.payWeek[i][0]) + ' ' + \
                     calendar.month_abbr[ppObj.payWeek[i][1]]            
            dayLbl = Label(row, font = labelFont, text = dayTxt, anchor = W, width = 12)
            inEntry = Entry(row, font = entryFont, width = 6, state = DISABLED)
            outEntry = Entry(row, font = entryFont, width = 6, state = DISABLED )
            inEntry.bind('<Button-1>', self.entrySelection) #remove selection of emp when move to entry box
            outEntry.bind('<Button-1>', self.entrySelection)
            
            inAm = Radiobutton(row, text = 'AM', fg = 'red', variable = self.AmPm[i][0], value = 1)
            inPm = Radiobutton(row, text = 'PM', fg = 'blue', variable = self.AmPm[i][0], value = 2)
            outAm = Radiobutton(row, text = 'AM', fg = 'red', variable = self.AmPm[i][1], value = 1)
            outPm = Radiobutton(row, text = 'PM', fg = 'blue', variable = self.AmPm[i][1], value = 2)
            self.AmPm[i][0].set(1)
            self.AmPm[i][1].set(2)
            inOutMatrix[i][0] = inEntry
            inOutMatrix[i][1] = outEntry
             
            dayLbl.pack(side = LEFT)
            inEntry.pack(side = LEFT)
            inAm.pack(side = LEFT)
            inPm.pack(side = LEFT)
            outEntry.pack(side = LEFT)
            outAm.pack(side = LEFT)
            outPm.pack(side = LEFT)
            row.pack(anchor = W)
            
        inOutMatrix[0][0].focus_set()
        self.inOutMatrix = inOutMatrix
        
        self.buttonFrame = Frame(self.container3, width = 850, height = 345, bd = 2, relief = RIDGE)
        self.buttonFrame.propagate(0)
        self.buttonFrame.pack(side = LEFT, anchor = N)

        row1 = Frame(self.buttonFrame)
        row1.pack(side = BOTTOM, anchor = W, fill = X)

        self.clearButton = Button(row1, text = 'Clear',font = buttonFont, width = 13, height = 3,
                             command = self.resetPayrollGui, state = DISABLED)        
        closeButton = Button(row1, text = 'Close', font = buttonFont, height = 3, width = 13,
                            command = self.closeGui)
             
        self.clearButton.pack(side = LEFT, anchor = S)  
        closeButton.pack(side = LEFT, anchor = S)
        
        self.modeFrame = Frame(self.buttonFrame, bd = 2, relief = RIDGE  ) #may not need to create ???????
        self.modeFrame.pack(side = TOP, anchor = W)
    
    def viewTimeGui(self):
        self.container1 = Frame(self.parent,width = 1250, height = 40)
        self.container1.propagate(0)
        self.container1.pack()
        
        Label(self.container1,text = 'eManagement System', font = ('times', 16, 'bold')).pack()
                       
        self.container2 = Frame(self.parent, width = 1250, height = 435, bd = 2, relief = RIDGE)
        self.container2.propagate(0)
        self.container2.pack()
        
        viewFrame = Frame(self.container2, width = 1250, height = 460,  bd = 2, relief = RIDGE)
        viewFrame.propagate(0)
        viewFrame.pack(anchor = W)
        
        self.timeSheetView = treeView(viewFrame, self.timeSheetHeading, timeSheetHeadingSize, 20)
        self.timeSheetView.tree.bind('<Double-1>', self.fetchClick)
            
        self.container3 = Frame(self.parent, width = 1250, height = 300, bd = 2, relief = RIDGE) #just a dummy container
        self.container3.propagate(0)
        self.container3.pack()
        
        row1 = Frame(self.container3, width = 625, height = 300)
        row1.pack(side = RIGHT, anchor = N)

        closeButton = Button(row1, text = 'Close', font = buttonFont, height = 3, width = 13,
                            command = self.closeGui)
        closeButton.pack(side = LEFT, anchor = N)
        
    def payrollDisplayGui(self, ppObj):
        self.container1 = Frame(self.parent,width = 1250, height = 40)
        self.container1.propagate(0)
        self.container1.pack()
        
        Label(self.container1,text = 'Payroll:  ', font = ('times', 16, 'bold')).pack(side = LEFT, anchor = S)
        payPeriodLbl = Label(self.container1, text = ppObj.payPeriod, font = ('arial', 12, 'bold'), fg = 'red')
        payPeriodLbl.pack(side = LEFT, anchor = S)   #text value is setup at payrollGui
              
        self.container2 = Frame(self.parent, width = 1250, height = 435, bd = 2, relief = RIDGE)
        self.container2.propagate(0)
        self.container2.pack()
        viewFrame = Frame(self.container2, width = 840, height = 430, bd = 2, relief = RIDGE)
        viewFrame.propagate(0)
        viewFrame.pack(side = LEFT)

        #columnHeading = ('Id',) + fieldName
        self.payrollView = treeView(viewFrame, payrollHeading, payrollHeadingSize, 20)
        self.payrollView.tree.bind('<Double-1>', self.fetchClick)
        #self.loadEmpData() # Loads emp data on tView with row colors    
        
        buttonFrame = Frame(self.container2, width = 410, height = 430, bd = 2, relief = RIDGE)
        buttonFrame.propagate(0)
        buttonFrame.pack(side = LEFT)

        row1 = Frame(buttonFrame)
        row1.pack(side = TOP, anchor = W)

        closeButton = Button(row1, text = 'Close', font = buttonFont, height = 3, width = 13,
                            command = self.closeGui)
        closeButton.pack(side = LEFT, anchor = N)
        '''clearButton = Button(row1, text = 'Clear',font = buttonFont, width = 13, height = 3,
                             command = self.clearForm)
        clearButton.pack(side = LEFT, anchor = N)'''
        self.container3 = Frame(self.parent, width = 1250, height = 300, bd = 2, relief = RIDGE) 
        self.container3.propagate(0)
        self.container3.pack()
        textFrame = Frame(self.container3)
        textFrame.pack(side = LEFT, anchor = N)
        self.payInfo = Text(textFrame, font = ('Verdana', 10 ), height = 18, width = 40)
        self.payInfo.pack(side = LEFT, anchor = N)
        printFrame = Frame(self.container3)
        printFrame.pack(side = LEFT, anchor = N)
        self.printButton = Button(printFrame, text = 'Print', font = buttonFont, height = 3, width = 13,
                             command = self.printPayrollInfo, state = DISABLED)
        self.printButton.pack(side = LEFT, anchor = N)
             
    def addEmpGui(self):
        if not self.mode:
            self.empDataDisplayGui()
            self.empDataEntryGui()
            addButton = Button(self.modeFrame, text = 'Add', width = 13, height = 3, font = buttonFont,
                               command = self.addEmp)
            addButton.pack(side = LEFT, anchor = N)
        elif self.mode == 'updateEmp':
            self.clearForm()
            self.modeFrame.destroy()
            self.modeFrame = Frame(self.buttonFrame)
            self.modeFrame.pack(side = TOP, anchor = W)
            addButton = Button(self.modeFrame, text = 'Add', width = 13, height = 3, font = buttonFont,
                               command = self.addEmp)
            addButton.pack(side = LEFT, anchor = N)
        elif self.mode in ('addTime', 'updateTime', 'payroll', 'viewTime'):
            #if self.mode != 'payroll':
            self.timeSheetDBObj.close() #closes time sheet database
            
            self.container1.destroy()
            self.container2.destroy()
            self.container3.destroy()
            
            self.empDataDisplayGui()
            self.empDataEntryGui()
            addButton = Button(self.modeFrame, text = 'Add', width = 13, height = 3, font = buttonFont,
                               command = self.addEmp)
            addButton.pack(side = LEFT, anchor = N)
        
        self.mode = 'addEmp'
        #print('mode: ', self.mode) 
        
    def updateEmpGui(self):
        if not self.mode:
            self.empDataDisplayGui()
            self.empDataEntryGui()
            
            updateButton = Button(self.modeFrame, text = 'Update', width = 13, height = 3,
                                  font = buttonFont, command = self.updateEmp)
            updateButton.pack(side = LEFT, anchor = N)
            deleteButton = Button(self.modeFrame, text = 'Delete', width = 13, height = 3,
                                  font = buttonFont, command = self.deleteEmp)
            deleteButton.pack(side = LEFT, anchor = N)
           
        elif self.mode == 'addEmp':
            self.clearForm()
            self.modeFrame.destroy()
            self.modeFrame = Frame(self.buttonFrame)
            self.modeFrame.pack(side = TOP, anchor = W)
            
            updateButton = Button(self.modeFrame, text = 'Update', width = 13, height = 3,
                                  font = buttonFont, command = self.updateEmp)
            updateButton.pack(side = LEFT, anchor = N)
            deleteButton = Button(self.modeFrame, text = 'Delete', width = 13, height = 3,
                                  font = buttonFont, command = self.deleteEmp)
            deleteButton.pack(side = LEFT, anchor = N)
           
        elif self.mode in ('addTime', 'updateTime', 'payroll', 'viewTime'):
            #if self.mode != 'payroll':            
            self.timeSheetDBObj.close() #closes time sheet database, when go out of addTime & updateTime
            
            self.container1.destroy()
            self.container2.destroy()
            self.container3.destroy()
            
            self.empDataDisplayGui()
            self.empDataEntryGui()
            
            updateButton = Button(self.modeFrame, text = 'Update', width = 13, height = 3,
                                  font = buttonFont, command = self.updateEmp)
            updateButton.pack(side = LEFT, anchor = N)
            deleteButton = Button(self.modeFrame, text = 'Delete', width = 13, height = 3,
                                  font = buttonFont, command = self.deleteEmp)
            deleteButton.pack(side = LEFT, anchor = N)
            
        
        self.mode = 'updateEmp'
        
        #print('mode: ', self.mode)
    
        
    def payrollGui(self): ## working *******************************************
        if self.mode != 'payroll':
            payPeriodObj = PayPeriod(self.parent, self.weekDayOrder)
            if payPeriodObj.select:
                self.payPeriod = payPeriodObj.startDate + ' to ' + payPeriodObj.endDate #only to print
                #self.startDate = payPeriodObj.startDate                                #on receipt
                #self.endDate = payPeriodObj.endDate #not used anywhere, may not need it????????????
                if not self.mode:
                    self.payrollDisplayGui(payPeriodObj)
                    self.payrollCalculation(payPeriodObj)
                
                elif self.mode in ('addEmp', 'updateEmp'):
                    self.container1.destroy()
                    self.container2.destroy()
                    self.container3.destroy()
                    self.payrollDisplayGui(payPeriodObj)
                    self.payrollCalculation(payPeriodObj)
                
                elif self.mode in ('addTime', 'updateTime', 'viewTime'): # viewTime not done???????????????**********
                    self.timeSheetDBObj.close() #closes time sheet database, when go out of addTime & updateTime
            
                    self.container1.destroy()
                    self.container2.destroy()
                    self.container3.destroy()
            
                    self.payrollDisplayGui(payPeriodObj)
                    self.payrollCalculation(payPeriodObj)
            
                self.mode = 'payroll'
        
        #print('mode: ', self.mode)
        
    def updateTimeGui(self):
        if self.mode in ('', 'addEmp', 'updateEmp', 'payroll', 'viewTime'):
            payPeriodObj = PayPeriod(self.parent, self.weekDayOrder)
            if payPeriodObj.select:
                
                self.setupTimeDB(payPeriodObj)
                
                if self.mode != '': # in ('addEmp' , 'updateEmp', 'payroll'):
                    self.container1.destroy()
                    self.container2.destroy()
                    #if self.mode in ('addEmp' , 'updateEmp'): ##don't need it if created dummy container3 for payroll
                    self.container3.destroy()
        
                self.timeDisplayGui()  #this and 
                self.timeEntryGui(payPeriodObj) #this could make separate class??************
                self.loadTimeData() #uses timeSheetDBObj
                
                self.updateTimeButton = Button(self.modeFrame, text = 'Update', state = DISABLED, font = buttonFont,
                        command = self.addTime, width = 13, height = 3)
                self.updateTimeButton.pack(side = LEFT, anchor = N)  
                self.deleteTimeButton = Button(self.modeFrame, text = 'Delete', state = DISABLED, font = buttonFont,
                        command = self.deleteTime, width = 13, height = 3)
                self.deleteTimeButton.pack(side = LEFT, anchor = N)
                              
                self.mode = 'updateTime'
                    
            
        elif self.mode == 'addTime':
            self.resetPayrollGui()
            self.disableTimeForm()
            self.modeFrame.destroy()
            self.modeFrame = Frame(self.buttonFrame)
            self.modeFrame.pack(side = TOP, anchor = W)
            
            self.updateTimeButton = Button(self.modeFrame, text = 'Update', state = DISABLED, font = buttonFont,
                               command = self.addTime, width = 13, height = 3)
            self.updateTimeButton.pack(side = LEFT, anchor = N)            
            self.deleteTimeButton = Button(self.modeFrame, text = 'Delete', state = DISABLED, font = buttonFont,
                               command = self.deleteTime, width = 13, height = 3)
            self.deleteTimeButton.pack(side = LEFT, anchor = N)
                        
            self.clearButton.configure(state = DISABLED)
            self.mode = 'updateTime'
        
        #print('mode: ', self.mode)
        
        
    def addTimeGui(self):
        if self.mode in ('', 'addEmp', 'updateEmp', 'payroll', 'viewTime'):
            payPeriodObj = PayPeriod(self.parent, self.weekDayOrder)
            if payPeriodObj.select:
                
                self.setupTimeDB(payPeriodObj)
                
                if self.mode != '':           # OR in ('addEmp' , 'updateEmp', 'payroll'):
                    self.container1.destroy()
                    self.container2.destroy()
                    self.container3.destroy()
                self.timeDisplayGui()  #this and 
                self.timeEntryGui(payPeriodObj) #this could make separate class??************
                self.loadTimeData() #uses timeSheetDBObj
                
                self.addTimeButton = Button(self.modeFrame, text = 'Add', state = DISABLED, font = buttonFont,
                               command = self.addTime, width = 13, height = 3)
                self.addTimeButton.pack(side = LEFT, anchor = N)
                self.clearButton.configure(state = DISABLED)
                self.mode = 'addTime'
            
        elif self.mode == 'updateTime':
            self.resetPayrollGui() #***change name????????
            self.disableTimeForm()
            self.modeFrame.destroy()
            self.modeFrame = Frame(self.buttonFrame)
            self.modeFrame.pack(side = TOP, anchor = W)
            self.addTimeButton = Button(self.modeFrame, text = 'Add', state = DISABLED, font = buttonFont,
                               command = self.addTime, width = 13, height = 3)
            self.addTimeButton.pack(side = LEFT, anchor = N)
            self.clearButton.configure(state = DISABLED)
            self.mode = 'addTime'

        #print('mode: ', self.mode)
        #print('week day order: ', self.weekDayOrder)
    
    def viewTime(self):
        
        payPeriodObj = PayPeriod(self.parent, self.weekDayOrder)
        if payPeriodObj.select:
            
            self.setupTimeDB(payPeriodObj)
            
            if self.mode != '': #in ('addEmp' , 'updateEmp', 'payroll'):
                self.container1.destroy()
                self.container2.destroy()
                self.container3.destroy()  
                
            self.viewTimeGui()
            self.loadTimeData() #uses timeSheetDBObj
            self.mode = 'viewTime'
            
        #print('mode: ', self.mode)
                    
    '''def timeGui(self, ppObj):
        self.payPeriod = ppObj.startDate + ' to ' + ppObj.endDate
        self.startDate = ppObj.startDate
        self.endDate = ppObj.endDate

        if self.mode in ('addEmp' , 'updateEmp', 'payroll'):
            self.container1.destroy()
            self.container2.destroy()
            #if self.mode in ('addEmp' , 'updateEmp'): ##don't need it if created dummy container3 for payroll
            self.container3.destroy()
        
        self.timeDisplayGui()  #this and 
        self.timeEntryGui(ppObj) #this could make separate class??************
                
        ##########################
        ## might need to modify here to make robust with emp list
        self.timeSheetDB = payrollDB + self.startDate.replace('/', '_')
            
        print('timesheetdb: ', self.timeSheetDB)
        ###good place for exception catch############
        self.timeSheetDBObj = shelve.open(self.timeSheetDB) #timeSheetDB can have data of deleted emp.
                                ####### So, create separate time data view and edit interface
                
        for key in employeeDB:
            if key not in self.timeSheetDBObj:
                self.timeSheetDBObj[key] = WeeklyTime()
        
        self.sizeOfTimeSheet()  #???????????     

        self.loadTimeData() #uses timeSheetDBObj
    '''
        
    def setupTimeDB(self, ppObj):
             
        self.timeSheetDB = payrollDB + ppObj.startDate.replace('/', '_')
        
        ###good place for exception catch############
        self.timeSheetDBObj = shelve.open('timeData/' + self.timeSheetDB) #timeSheetDB can have data of deleted emp.
                                ####### So, create separate time data view and edit interface
        #if self.mode != 'viewTime':        
        for key in employeeDB:  
            if key not in self.timeSheetDBObj: #***This loop adds new emp to old timesheetDB????
                self.timeSheetDBObj[key] = WeeklyTime()
            
        #self.sizeOfEmpDB()
        #self.sizeOfTimeSheet()
        
    def payrollCalculation(self, ppObj):##working on??????????????????
       
        self.timeSheetDB = payrollDB + ppObj.startDate.replace('/', '_')
         
        ###good place for exception catch############
        self.timeSheetDBObj = shelve.open('timeData/' + self.timeSheetDB) #timeSheetDB can have data of deleted emp.
                                ####### So, create separate time data view and edit interface
                
        for i, key in enumerate(employeeDB):
            if key not in self.timeSheetDBObj: #this adds new emp to old timeSheetDB just like setupTimeDB
                self.timeSheetDBObj[key] = WeeklyTime()
            weeklyTimeObj = self.timeSheetDBObj[key] #update member data of this objects
            
            weeklyTimeObj.rate = employeeDB[key].payRate
            weeklyTimeObj.totalHour = weeklyTimeObj.getWeeklyHour()
            if weeklyTimeObj.totalHour > Decimal('40'):
                weeklyTimeObj.overTime = weeklyTimeObj.totalHour - Decimal('40')
                weeklyTimeObj.regularHour = Decimal('40')
            else:
                weeklyTimeObj.overTime = 0
                weeklyTimeObj.regularHour = weeklyTimeObj.totalHour
            
            #weeklyTimeObj.overTimeRate = employeeDB[key].overTimeRate #**This doesn't updates automatic**
            weeklyTimeObj.overTimeRate = employeeDB[key].getOTRate()
            weeklyTimeObj.totalPay = weeklyTimeObj.getTotalPay()
            
            del self.timeSheetDBObj[key]             #delete old object
            self.timeSheetDBObj[key] = weeklyTimeObj #store updated object
            
            payData = (key, employeeDB[key].name, weeklyTimeObj.totalHour, weeklyTimeObj.regularHour,
                       weeklyTimeObj.overTime, weeklyTimeObj.rate, weeklyTimeObj.overTimeRate, weeklyTimeObj.totalPay, 0)
            self.displayData(i, payData, self.payrollView.tree)
            
            '''print('reg: ', self.timeSheetDBObj[key].regularHour)
            print('ot : ', self.timeSheetDBObj[key].overTime)            
            print('rate: ', self.timeSheetDBObj[key].rate)
            print('ot rate: ', self.timeSheetDBObj[key].overTimeRate)
            print('total hour: ', self.timeSheetDBObj[key].totalHour)
            print('total pay : ', self.timeSheetDBObj[key].totalPay)
            print()
            '''
        
    def sizeOfTimeSheet(self): #can make return the size
        print ('Size of TimeSheet: ', len([1 for key in self.timeSheetDBObj])) 
        
    def sizeOfEmpDB(self):
        print ('Size of empDB: ', len([1 for key in employeeDB]))           
        
    def addTime(self):
        weeklyTimeObj = self.timeSheetDBObj[self.fetchedEmp]
        timeArray = [''] * 7
        
        for i in range(7):
            if self.inOutMatrix[i][0].get() and self.inOutMatrix[i][1].get():
                try:
                    inTime = Decimal(str(self.inOutMatrix[i][0].get())).quantize(Decimal('0.01')) #value from Entry object is string
                    outTime = Decimal(str(self.inOutMatrix[i][1].get())).quantize(Decimal('0.01'))
                    #inTime = inTime.quantize(Decimal('0.01'))     
                    #outTime = outTime.quantize(Decimal('0.01')) 
                except:
                    showinfo('', 'Didn\'t enter proper number for \"' + calendar.day_name[(i+6)%7] + '\"\nEnter again.')
                    continue
                
                tInH = inTime // Decimal('1')  #old code: tInH = inTime * 100 // 100
                tInM = inTime % Decimal('1') # old code: tInM = inTime * 100 % 100
                
                tOutH = outTime // Decimal('1') # old code: tOutH = outTime * 100 // 100
                tOutM = outTime % Decimal('1')  # old code: tOutM = outTime * 100 % 100
                
                inAm = int(self.AmPm[i][0].get())
                outPm = int(self.AmPm[i][1].get())                
                
                #weeklyTimeObj.setDailyTime(self.weekDayOrder[i].lower(), tInH, tInM, inAm, tOutH, tOutM, outPm)# This allows to store time data
                weeklyTimeObj.setDailyTime(self.weekDayOrder[i], tInH, tInM, inAm, tOutH, tOutM, outPm)# This allows to store time data
                #this is good for 1st time entering but for secondtime and later to add additional time
                #this does not show older times
            elif self.weekDayOrder[i] in weeklyTimeObj.dailyTimeObj: # remove the day from the weeklyTime object
                del weeklyTimeObj.dailyTimeObj[self.weekDayOrder[i]] # if old time  is deleted when updating
                                                
        for day in weeklyTimeObj.dailyTimeObj:
            timeArray[self.weekDayOrder.index(day)] = self.displayTime(weeklyTimeObj.dailyTimeObj[day])
        
        del self.timeSheetDBObj[self.fetchedEmp] #Delete existing time data
        self.timeSheetDBObj[self.fetchedEmp] = weeklyTimeObj #Store the updated time data only into DB, other member data
                                                        #weeklyTime object are initialized at payrollCalculation()
        ###modify this
        timeData = (self.fetchedEmp, employeeDB[self.fetchedEmp].name, timeArray[0], timeArray[1], timeArray[2],
                    timeArray[3], timeArray[4], timeArray[5], timeArray[6], weeklyTimeObj.getWeeklyHour())
        index = self.timeSheetView.tree.index(self.fetchedEmp)
        self.timeSheetView.tree.delete(self.fetchedEmp) #This will also remove focus from the item
        #self.timeSheetView.tree.insert('', index, iid = self.fetchedEmp, values = timeData, tags = index%2)
        #self.setRowBGColor(index, self.timeSheetView.tree)
        self.displayData(index, timeData, self.timeSheetView.tree)   #instead of obove two statements     
        
        if self.mode == 'addTime':
            self.addTimeButton.configure(state = DISABLED)
        elif self.mode == 'updateTime':
            self.updateTimeButton.configure(state = DISABLED)
            self.deleteTimeButton.configure(state = DISABLED)
            
        self.clearButton.configure(state = DISABLED)
        self.clearTimeForm()
        self.disableTimeForm()

    def addEmp(self):
        name = self.entries['Name'].get().upper()
        if name:
            empId = self.idGenerator(name)
            street = self.entries['Street'].get()
            city = self.entries['City'].get()
            state = self.entries['State'].get()
            zipCode = self.entries['ZIP'].get()
            phone = self.entries['Phone'].get()
            pRate = self.entries['Pay Rate'].get()
            if self.isNumber(pRate):
                pRate = Decimal(pRate).quantize(Decimal('.01'))
            else:
                 pRate = Decimal('0.00')
                 
            record = Employee(empId, name, street, city, state, zipCode, phone, pRate)
            empData = (empId, name, street, city, state, zipCode, phone, pRate)
            
            self.displayData(self.getLastIndex(), empData, self.tView.tree) #Insert new employee at top of list
            employeeDB[empId] = record
            
            self.clearForm()
        else:
            showinfo('Empty Name', 'Name can\'t be blank. Enter again.')

    def updateEmp(self):
        name = self.entries['Name'].get()
        if name:
            empId = self.fetchedEmp
            street = self.entries['Street'].get()
            city = self.entries['City'].get()
            state = self.entries['State'].get()
            zipCode = self.entries['ZIP'].get()
            phone = self.entries['Phone'].get()
            pRate = Decimal(self.entries['Pay Rate'].get()).quantize(Decimal('.01'))
            record = Employee(empId, name, street, city, state, zipCode, phone, pRate)
            empData = (empId, name, street, city, state, zipCode, phone, pRate)
            del employeeDB[self.fetchedEmp]
            employeeDB[empId] = record
            index = self.tView.tree.index(self.fetchedEmp)
            self.tView.tree.delete(self.fetchedEmp)
            #self.tView.tree.insert('', index, iid = empId, values = empData, tags = index%2)
            #self.setRowBGColor(index, self.tView.tree)
            self.displayData(index, empData, self.tView.tree) #instead of obove two statements
            self.clearForm()
            
        else:
            showinfo('Empty Name', 'Name can\'t be blank. Enter again.')
            
    def setRowBGColor(self, row, tView):
        if row%2 == 0:
            tView.tag_configure(0, background = '#e5f7ff')
        else:
            tView.tag_configure(1, background = '#e0ebeb')
            
    def getLastIndex(self):
        self.tView.tree.insert('', 'end', 'END')
        lastIndex = self.tView.tree.index('END')
        self.tView.tree.delete('END')
        return lastIndex
        
    def displayData(self, index, empData, tView):
        tView.insert('', index, iid = empData[0], values = empData, tags = index%2)
        self.setRowBGColor(index, tView)
        
    def loadEmpData(self):
        for i, key in enumerate(employeeDB):
            empData = (key, employeeDB[key].name, employeeDB[key].street, employeeDB[key].city, employeeDB[key].state,
                       employeeDB[key].zipCode, employeeDB[key].phone, employeeDB[key].payRate)
            self.displayData(i, empData, self.tView.tree)
            
        
    def reloadEmpData(self):  #used in deleting emp data
        for key in employeeDB:
            empData = (key, employeeDB[key].name, employeeDB[key].street, employeeDB[key].city, employeeDB[key].state,
                       employeeDB[key].zipCode, employeeDB[key].phone, employeeDB[key].payRate)
            index = self.tView.tree.index(key)
            self.tView.tree.delete(key)
            self.displayData(index, empData, self.tView.tree)
            
         
    def loadTimeData(self): #call in only one place
        for i, key in enumerate(employeeDB):  ##(self.timeSheetDBObj): to display only current emp time
            timeArray = [''] * 7 #could make dictionary instead??????????
            
            weeklyObj = self.timeSheetDBObj[key]
            for day in weeklyObj.dailyTimeObj:
                timeArray[self.weekDayOrder.index(day)] = self.displayTime(weeklyObj.dailyTimeObj[day])
                    
            timeData = (key, employeeDB[key].name, timeArray[0], timeArray[1], timeArray[2], timeArray[3],
                       timeArray[4], timeArray[5], timeArray[6], weeklyObj.getWeeklyHour())
            #self.timeSheetView.tree.insert('','end', iid = key, values = timeData, tags = i%2)
            #self.setRowBGColor(i, self.timeSheetView.tree)
            self.displayData(i, timeData, self.timeSheetView.tree) #instead of two above statements
        #print('Load Time:')
        #self.sizeOfEmpDB()
        #self.sizeOfTimeSheet()        

    def displayTime(self, dailyTimeObj):
        timeIn = str(dailyTimeObj.getTimeInHour() + dailyTimeObj.getTimeInMinute()).replace('.', ':') #conver to display format
        timeOut = str(dailyTimeObj.getTimeOutHour() + dailyTimeObj.getTimeOutMinute()).replace('.', ':')
        if dailyTimeObj.inAm == 1:
            timeIn = timeIn + 'AM'
        else:
            timeIn = timeIn + 'PM'
        if dailyTimeObj.outPm == 2:
            timeOut = timeOut + 'PM'
        else:
            timeOut = timeOut + 'AM'
                        
        return (timeIn + '-' + timeOut + '='+ str(dailyTimeObj.totalHours))  
    
    def fetchEmp(self):
        fetchedEmp = self.tView.tree.focus() #self.tView is not a Treeview object but self.tVeiw.tree is.
        
        if fetchedEmp:
            self.clearForm()
            self.idValue.configure(text = fetchedEmp)
            
            self.entries['Name'].insert(0, employeeDB[fetchedEmp].name)
            self.entries['Street'].insert(0, employeeDB[fetchedEmp].street)
            self.entries['City'].insert(0, employeeDB[fetchedEmp].city)
            self.entries['State'].insert(0, employeeDB[fetchedEmp].state)
            self.entries['ZIP'].insert(0, employeeDB[fetchedEmp].zipCode)
            self.entries['Phone'].insert(0, employeeDB[fetchedEmp].phone)
            self.entries['Pay Rate'].insert(0, employeeDB[fetchedEmp].payRate)
            
            self.fetchedEmp = fetchedEmp #make it accessible from other methods like in updateEmp()
        else:
            showinfo('Update Item', 'First, click the name you want to update. Try again.')
    
    def fetchTimeSheet(self):
        self.fetchedEmp = self.timeSheetView.tree.focus()
            
        if self.fetchedEmp:
            self.enableTimeForm()
            if self.mode == 'addTime':
                self.empIDVal.configure(text = self.fetchedEmp)
                self.empNameVal.configure(text = employeeDB[self.fetchedEmp].name)
                self.addTimeButton.configure(state = NORMAL)
                self.clearButton.configure(state = NORMAL)
            elif self.mode == 'updateTime':
                self.clearTimeForm()
                valList = self.timeSheetView.tree.item(self.fetchedEmp,('values',))
                self.empIDVal.configure(text = self.fetchedEmp)
                self.empNameVal.configure(text = employeeDB[self.fetchedEmp].name)
                
                for i in range(2, 9):
                    if valList[i]:
                        inTime, outTime = valList[i].split('-') #don't need index
                        outTime = outTime.split('=')[0] #need index here
                        inAmPm = inTime[-2: ] #this need to do first before next step
                        inTime = inTime[ : len(inTime) -2]#inTime.split(' ') if like 10:30 AM
                        
                        outAmPm = outTime[-2: ]
                        outTime = outTime.split(outAmPm)[0] #need index 0 here
                        inTime = inTime.replace(':', '.')
                        outTime = outTime.replace(':', '.')
                        
                        self.inOutMatrix[i-2][0].insert(0, inTime)
                        self.inOutMatrix[i-2][1].insert(0, outTime)
                        if inAmPm == 'AM':
                            self.AmPm[i-2][0].set(1)
                        else:
                            self.AmPm[i-2][0].set(2)
                        if outAmPm == 'PM':
                            self.AmPm[i-2][1].set(2)
                        else:
                            self.AmPm[i-2][1].set(1)
                     
                self.updateTimeButton.configure(state = NORMAL)
                self.deleteTimeButton.configure(state = NORMAL)
                self.clearButton.configure(state = NORMAL)
                
    def printPayrollInfo(self):
        #old format
        '''filename = tempfile.mktemp('.txt')
        f = open (filename, 'w')
        #f.write('\n')
        printer_name = win32print.GetDefaultPrinter ()
        hPrinter = win32print.OpenPrinter (printer_name)
        f.write('{0:<8s}{1:<10s}\n'.format('Name: ', employeeDB[self.fetchedEmp].name))
        f.write('{0:<8s}{1:<10s}\n\n'.format('ID:  ', self.fetchedEmp))
        f.write('  ' + self.payPeriod + '\n')
                    
        if float(self.payVal[2]) <= 40.00:
            f.write('-' * 26 + '\n\n')
            f.write('{0:<15s}{1:>10.2f}\n'.format('Total Hours: ', float(self.payVal[2])))
            totalPay = self.payVal[2] + ' X ' + self.payVal[5] + ' = $' + self.payVal[7]
            f.write('{0:<15s}\n'.format('Total Pay: '))
            f.write('  {0:<35s}\n'.format(totalPay))
        else:
            f.write('-' * 41 + '\n\n')
            f.write('{0:<15s}{1:>10.2f}\n'.format('Total Hours: ', float(self.payVal[2])))
            totalPay = '40' + ' X ' + self.payVal[5] + ' + ' + self.payVal[4] + \
                    ' X ' + self.payVal[6] + ' = $' + self.payVal[7]
            f.write('{0:<15s}{1:>10.2f}\n'.format('Regular Hours: ', 40.00))
            f.write('{0:<15s}{1:>10.2f}\n'.format('Over Time: ', float(self.payVal[4])))
            f.write('{0:<15s}\n'.format('Total Pay: '))
            f.write('{0:35s}\n'.format(totalPay))
            
            #f.write('\n\n')
                        
        f.close()
        #print ('hello', file = hPrinter )
        win32api.ShellExecute ( None, "print", filename,  '/d:"%s"' % hPrinter,  ".",  0 )
        '''
             
        ##### New Format ###########
        # X from the left margin, Y from top margin
        # both in pixels
        X=80; Y=100
        printer_name = win32print.GetDefaultPrinter ()
        
        hDC = win32ui.CreateDC ()
        hDC.CreatePrinterDC (printer_name)
        hDC.StartDoc ('PayDoc') #print this name on printer spool
        hDC.StartPage ()
        
        ##############
        payReciept = ('{0:<8s}{1:<10s}\n'.format('Name: ', employeeDB[self.fetchedEmp].name))
        payReciept = payReciept + ('{0:<8s}{1:<10s}\n\n'.format('ID:  ', self.fetchedEmp))
        payReciept = payReciept + ('from ' + self.payPeriod + '\n')
        payReciept = payReciept + ('-' * 41 + '\n\n')            
        if float(self.payVal[2]) <= 40.00:
            #payReciept = payReciept + ('-' * 26 + '\n\n')
            payReciept = payReciept + ('{0:<15s}{1:>10.2f}\n'.format('Total Hours: ', float(self.payVal[2])))
            totalPay = self.payVal[2] + ' X ' + self.payVal[5] + ' = $' + self.payVal[7]
            payReciept = payReciept + ('{0:<15s}\n'.format('Total Pay: '))
            payReciept = payReciept + ('{0:<35s}\n'.format(totalPay))
        else:
            #payReciept = payReciept + ('-' * 41 + '\n\n')
            payReciept = payReciept + ('{0:<15s}{1:>10.2f}\n'.format('Total Hours: ', float(self.payVal[2])))
            totalPay = '40' + ' X ' + self.payVal[5] + ' + ' + self.payVal[4] + \
                    ' X ' + self.payVal[6] + ' = $' + self.payVal[7]
            payReciept = payReciept + ('{0:<15s}{1:>10.2f}\n'.format('Regular Hours: ', 40.00))
            payReciept = payReciept + ('{0:<15s}{1:>10.2f}\n'.format('Over Time: ', float(self.payVal[4])))
            payReciept = payReciept + ('{0:<15s}\n'.format('Total Pay: '))
            payReciept = payReciept + ('{0:35s}\n'.format(totalPay))

        payReciept = payReciept + ('\n' * 10 + '\n') 
        payReciept = payReciept + ('{0:^40s}\n'.format('Thank You.'))
        
        ################        
        payRecieptList = payReciept.split('\n')
        for line in payRecieptList:
            hDC.TextOut(X,Y,line)
            Y += 100
        hDC.EndPage ()
        hDC.EndDoc ()
        
        self.payInfo.configure(state = NORMAL)  
        self.payInfo.delete('1.0', END)
        self.payInfo.configure(state = DISABLED) 
        self.printButton.configure(state = DISABLED)
        
    def fetchPayrollInfo(self):
        self.fetchedEmp = self.payrollView.tree.focus()
            
        if self.fetchedEmp:
            self.printButton.configure(state = NORMAL)
            self.payInfo.configure(state = NORMAL)  
            self.payInfo.delete('1.0', END)
            self.payVal = self.payrollView.tree.item(self.fetchedEmp,('values',))
                #self.empIDVal.configure(text = self.fetchedEmp)
                #self.empNameVal.configure(text = employeeDB[self.fetchedEmp].name)
            self.payInfo.insert(END, '\n')
            self.payInfo.insert(END, '\n')
            self.payInfo.insert(END,'{0:<8s}{1:<10s}\n'.format('  Name: ', employeeDB[self.fetchedEmp].name))
            self.payInfo.insert(END,'{0:<10s}{1:<10s}\n\n'.format('  ID:  ', self.fetchedEmp))
            self.payInfo.insert(END, '  ' + self.payPeriod + '\n')
            #self.payInfo.insert(END, ' ' + '-' * 41 + '\n')
            #self.payInfo.insert(END, '\n')
            #self.payInfo.insert(END,'{0:<15s}{1:>5.2f}\n'.format('  Total Hours: ', float(self.payVal[2])))
            
            if float(self.payVal[2]) <= 40.00:
                self.payInfo.insert(END, ' ' + '-' * 24 + '\n\n')
                self.payInfo.insert(END,'{0:<15s}{1:>10.2f}\n'.format('  Total Hours: ', float(self.payVal[2])))
                totalPay = self.payVal[2] + ' X ' + self.payVal[5] + ' = $' + self.payVal[7]
                self.payInfo.insert(END,'{0:<15s}\n'.format('  Total Pay: '))
                self.payInfo.insert(END,'  {0:<35s}\n'.format(totalPay))
            else:
                self.payInfo.insert(END, ' ' + '-' * 40 + '\n\n')
                self.payInfo.insert(END,'{0:<15s}{1:>10.2f}\n'.format('  Total Hours: ', float(self.payVal[2])))
                totalPay = '40' + ' X ' + self.payVal[5] + ' + ' + self.payVal[4] + \
                            ' X ' + self.payVal[6] + ' = $' + self.payVal[7]
                self.payInfo.insert(END,'{0:<15s}{1:>10.2f}\n'.format('  Regular Hours: ', 40.00))
                self.payInfo.insert(END,'{0:<15s}{1:>10.2f}\n'.format('  Over Time: ', float(self.payVal[4])))
                self.payInfo.insert(END,'{0:<15s}\n'.format('  Total Pay: '))
                self.payInfo.insert(END,'  {0:35s}\n'.format(totalPay))
            
            self.payInfo.configure(state = DISABLED)  
         
    def fetchClick(self, event):
        if self.mode in ('addTime', 'updateTime'):
            self.fetchTimeSheet()
               
        elif self.mode == 'payroll':
            self.fetchPayrollInfo()            
            
        elif self.mode == 'updateEmp':
            self.fetchEmp()
     
    def deleteEmp(self):
        empToDelete = self.tView.tree.focus() #self.tView is not a Treeview object but self.tVeiw.tree is.
        if empToDelete:
            ans = askquestion('Delete?', 'Do you want to delete => ' + employeeDB[empToDelete].name)
            if ans == 'yes':
                self.tView.tree.delete(empToDelete)
                del employeeDB[empToDelete]
                
                self.reloadEmpData()
            self.clearForm()
            
        else:
            showinfo('Delete Item', 'First, click the name you want to delete. Try again.')
            
    def deleteTime(self):
        timeToDelete = self.timeSheetView.tree.focus()   #self.timeSheetView is not a Treeview object but
        if timeToDelete:                                 #self.timeSheetVeiw.tree is.
            ans = askquestion('Delete?', 'Do you want to delete?')
            if ans == 'yes':
                del self.timeSheetDBObj[timeToDelete] #Delete existing time data
                self.timeSheetDBObj[timeToDelete] = WeeklyTime() #Store new Weekly obj into DB
                
                timeData = (timeToDelete, employeeDB[timeToDelete].name, '', '', '', '', '', '', '', 0)
                index = self.timeSheetView.tree.index(timeToDelete)
                self.timeSheetView.tree.delete(timeToDelete) #This will also remove focus from the item
                self.displayData(index, timeData, self.timeSheetView.tree) #instead of obove & to adjust BG color
            self.updateTimeButton.configure(state = DISABLED)
            self.deleteTimeButton.configure(state = DISABLED)
            self.clearButton.configure(state = DISABLED)
            self.clearTimeForm()
            self.disableTimeForm()
        else:
            showinfo('Delete Item', 'First, click the name you want to delete. Try again.')
            
    def idGenerator(self, name):
        if len(name) < 3:
            name = name + 'ABC'
            
        while True:
            for i in range(10000):
                empId = name[0:3] + str(i)
                if empId not in employeeDB:
                    return empId
            return 'notValid'
            
    '''def setTimeSheetHeading(self):
        print('time sheet heading: ',self.timeSheetHeading)
        if not self.timeSheetHeading:      
            if not weekDayOrder:
                MonthlyCalender.setWeeklyDay(firstDay)
            
            timeSheetHeading = ('Id', 'Name')  + weekDayOder + ('Total',)
            print('time sheet heading: ',timeSheetHeading)
    '''

        
    def clearForm(self):        
        for key in self.entries:
            self.entries[key].delete(0, END)
        self.entries['Name'].focus_set()
        self.idValue.configure(text = '')
        
        
    def resetAmPm(self):
        for i in range(7):
            self.AmPm[i][0].set(1)
            self.AmPm[i][1].set(2)

    def disableTimeForm(self):
        for i in range(7):
            self.inOutMatrix[i][0].configure(state = DISABLED)
            self.inOutMatrix[i][1].configure(state = DISABLED)

    def enableTimeForm(self):
        for i in range(7):
            self.inOutMatrix[i][0].configure(state = NORMAL)
            self.inOutMatrix[i][1].configure(state = NORMAL)
        self.inOutMatrix[0][0].focus_set()
        
    def clearTimeForm(self):        
        for i in range(7):
            self.inOutMatrix[i][0].delete(0, END)
            self.inOutMatrix[i][1].delete(0, END)
        self.inOutMatrix[0][0].focus_set()
        self.empIDVal.configure(text = '')
        self.empNameVal.configure(text = '')
        self.resetAmPm()
        
    def resetPayrollGui(self):
        self.clearTimeForm()
        self.clearSelection()   #is this neccessary?????????
    
    
        
    def clearSelection(self): #work for payroll*****************
        if self.mode in ('addTime', 'updateTime'):
            selection = self.timeSheetView.tree.focus()
        
            if selection:
                index = self.timeSheetView.tree.index(selection)
                empData = self.timeSheetView.tree.item(selection)['values']
                #OR empData = self.timeSheetView.tree.item(selection, ('values'))
                self.timeSheetView.tree.delete(selection)
                self.displayData(index, empData, self.timeSheetView.tree)
        elif self.mode in ('addEmp', 'updateEmp'):           
            selection = self.tView.tree.focus()
            
            if selection:
                index = self.tView.tree.index(selection)
                empData = self.tView.tree.item(selection, ('values',))
                #OR empData = self.tView.tree.item(selection)['values']
                self.tView.tree.delete(selection)
                self.displayData(index, empData, self.tView.tree) #instead of oove two this one call is better
              
                
    def entrySelection(self, event): #when click on any emp data entry box, selection on emp name is removed
        self.clearSelection()
        
    def cancelPayEntry(self):
        self.payrollEntryFrame.destroy()
        self.timeSheetFrame.destroy()
        self.resetGui()
                           
    def closeGui(self): #make sure everything is in initial state****************
        self.resetGlobalVars()
        self.container1.destroy()
        self.container2.destroy()
        self.container3.destroy()
            
        self.closeDB()
        
    def resetGlobalVars(self):
        self.mode = ''
        self.fetchedEmp = ''
        
        
    def closeDB(self):
        if self.timeSheetDB:
                self.timeSheetDBObj.close()
        
    def quitProgram(self):
        ans = askquestion('Closing?', 'Do want to close the Program? ')
        if ans == 'yes':
            self.parent.destroy()
            employeeDB.close()
            self.closeDB()
    
    def isNumber(self, strVal):
        try:
            float(strVal)
            return True
        except ValueError:
            return False
            


if __name__ == '__main__':
    
    g = HRWin(Tk())
    g.mainloop()
    
    '''###############
    working on .selection_toggle in treeView, difference between focus and selection
    
    **global make dictionary of mode, so can be extensible
    ##############'''



