from tkinter import *
from calenderGui import MonthlyCalender
import calendar
from datetime import date

firstDay = 5 #need to have some value for all module, use global setting for 'setfirstweekday()' at beginning

class PayPeriod:
    def __init__(self, parent = None, dayOrder = ''):
        self.parent = parent
        #calendar.setfirstweekday(firstDay) # not neccessart if this setting is done in MonthlyCalender
        self.select = ''                   # before use of weekdays, it is to make sure
        self.payWeek = [[0] * 3 for i in range(7)] # list comprehension for 7X3 array
        self.payPeriod = ''
        self.startDate, self.endDate = self.currentPayPeriod()
        self.payPeriodGui(dayOrder)
        
    def payPeriodGui(self, dayOrder):
        
        self.dateWin = Toplevel(width = 460, height = 360)
        self.dateWin.title('Pay Period')
        self.dateWin.propagate(0)
        row1 = Frame(self.dateWin)
        row1.pack(anchor = W)
        self.payPeriodLbl1 = Label(row1, text = 'Pay Period: ' , font = ('arial', 12))
        self.payPeriodLbl2 = Label(row1, font = ('arial', 12, 'bold'), fg = 'red')
        self.payPeriodLbl1.pack(side = LEFT)
        self.payPeriodLbl2.pack(side = RIGHT)
        
        row2 = Frame(self.dateWin, bd = 2, relief = RIDGE, width = 364, height = 326)
        row2.propagate(0)
        row2.pack(side = LEFT, anchor = W)

        col1 = Frame(self.dateWin, bd = 2, relief = RIDGE, width = 95, height = 326)
        col1.pack(side = LEFT)
        col1.propagate(0)
        nextButton = Button(col1, text = 'Next\nPay Period', height = 3, width = 80,
                            command = self.nextPayPeriod)
        nextButton.pack()
        prevButton = Button(col1, text = 'Previous\nPay Period', height = 3, width = 80,
                            command = self.previousPayPeriod)
        prevButton.pack()
        
        okButton = Button(col1, text = 'Select', height = 3, width = 80, command = self.selectPeriod)
        okButton.pack(side = BOTTOM)
        cancelButton = Button(col1, text = 'Cancel', height = 3, width = 80, command = self.cancel)
        cancelButton.pack()
        
        self.payCalender = MonthlyCalender(row2, dayOrder) #make sure call calendar.setfirstweekday(firstDay) first
        self.payCalender.calenderFrame.pack()
        self.payPeriodLbl2.configure(text = self.payPeriod)

        
        self.dateWin.focus_set()
        self.dateWin.grab_set()
        self.dateWin.wait_window()
        
    def selectPeriod(self):
        self.select = 'yes'
        self.dateWin.destroy()
        
    def cancel(self):
        self.select = ''
        self.dateWin.destroy()
        
    def setPayPeriod(self):
        self.payPeriod = self.startDate + ' to ' + self.endDate
        
    def currentPayPeriod(self):
        d = date.today()
        d = d.timetuple()
        
        year = d[0] 
        month = d[1]
        day = d[2]
        #todayIs = d[6]
        
        monthCal = calendar.monthcalendar(year, month)
            
        for i in range(len(monthCal)):
            if day in monthCal[i]:
                week = monthCal[i]
                break
        
        if 0 in week:
            if week[0] == 0:
                sMonth = month - 1
                sYear = year
                if sMonth == 0:
                    sMonth = 12
                    sYear = year -1
                daysInPMonth = calendar.monthrange(sYear, sMonth)[1]
                
                eMonth = month
                eYear = year
                
                counter = 0
                for i in list(range(6, -1, -1)):
                    if week[i]:
                        self.payWeek[i][0] = week[i]
                        self.payWeek[i][1] = eMonth
                        self.payWeek[i][2] = eYear
                    else:
                        self.payWeek[i][0] = daysInPMonth - counter
                        self.payWeek[i][1] = sMonth
                        self.payWeek[i][2] = sYear
                        counter = counter + 1
            else:
                sMonth = month
                sYear = year
                
                eMonth = month + 1
                eYear = year
                if eMonth == 13:
                    eMonth = 1
                    eYear = year + 1
                counter = 1
                for i in range(7):
                    if week[i]:
                        self.payWeek[i][0] = week[i]
                        self.payWeek[i][1] = sMonth
                        self.payWeek[i][2] = sYear
                    else:
                        self.payWeek[i][0] = counter
                        self.payWeek[i][1] = eMonth
                        self.payWeek[i][2] = eYear
                        counter = counter + 1
        else:
            sMonth = eMonth = month
            sYear = eYear = year
            for i in range(7):
                self.payWeek[i][0] = week[i]
                self.payWeek[i][1] = sMonth
                self.payWeek[i][2] = sYear
                
        #for i in range(len(self.payWeek)):
            #print('curent week: ', self.payWeek[i])        
        #self.sMonth = sMonth
        #self.sYear = sYear
        #self.eMonth = eMonth
        #self.eYear = eYear
        
        self.startDate = str(self.payWeek[0][1]) + '/' + str(self.payWeek[0][0]) + '/' + str(self.payWeek[0][2])
        self.endDate = str(self.payWeek[6][1]) + '/' + str(self.payWeek[6][0]) + '/' + str(self.payWeek[6][2])
        self.setPayPeriod()
        
        #self.payPeriodLbl2.configure(text = self.startDate + '   to  ' + self.endDate)
        
        
        return self.startDate, self.endDate
    
        
    def nextPayPeriod(self):
        #eMonth = self.endDate.split('/')[0]
        #eDay = self.endDate.split('/')[1]
        #eYear = self.endDate.split('/')[2]
        self.payWeek[0][0] = self.payWeek[6][0] + 1
        self.payWeek[0][1] = self.payWeek[6][1]
        self.payWeek[0][2] = self.payWeek[6][2]
        #self.sMonth = self.eMonth
        #self.sYear = self.eYear
        daysInMonth = calendar.monthrange(self.payWeek[0][2], self.payWeek[0][1])[1]
        
        if self.payWeek[0][0] <= daysInMonth:
            nextDay = self.payWeek[0][0] + 1
            for i in range(6):
                if nextDay <= daysInMonth:
                    self.payWeek[i + 1][0] = nextDay
                    self.payWeek[i + 1][1] = self.payWeek[0][1]
                    self.payWeek[i + 1][2] = self.payWeek[0][2]
                    nextDay = nextDay + 1
                else:
                    self.payWeek[i + 1][0] = nextDay - daysInMonth
                    nextDay = nextDay + 1
                               
            if self.payWeek[0][0] > self.payWeek[6][0]:
                self.payWeek[6][1] = self.payWeek[6][1] + 1
                if self.payWeek[6][1] == 13:
                    self.payWeek[6][1] = 1
                    self.payWeek[6][2] = self.payWeek[6][2] + 1
                for i in range(7 - self.payWeek[6][0], 6):
                    self.payWeek[i][1] = self.payWeek[6][1]
                    self.payWeek[i][2] = self.payWeek[6][2]
        else:
            self.payWeek[0][1] = self.payWeek[0][1] + 1
            if self.payWeek[0][1] == 13:
                self.payWeek[0][1] = 1
                self.payWeek[0][2] = self.payWeek[0][2] + 1
            #self.payWeek[6][1] = self.payWeek[0][1]
            #self.payWeek[6][2] = self.payWeek[0][2]
            
            for i in range(7):
                self.payWeek[i][0] = i + 1
                self.payWeek[i][1] = self.payWeek[0][1]
                self.payWeek[i][2] = self.payWeek[0][2]
            
        self.startDate = str(self.payWeek[0][1]) + '/' + str(self.payWeek[0][0]) + '/' + str(self.payWeek[0][2])
        self.endDate = str(self.payWeek[6][1]) + '/' + str(self.payWeek[6][0]) + '/' + str(self.payWeek[6][2])
        self.setPayPeriod()        
        self.payPeriodLbl2.configure(text = self.payPeriod)
        
          
    def previousPayPeriod(self): 

        self.payWeek[6][0] = self.payWeek[0][0] - 1
        self.payWeek[6][1] = self.payWeek[0][1] 
        self.payWeek[6][2] = self.payWeek[0][2]
        #self.eMonth = self.sMonth
        #self.eYear = self.sYear
        
        if self.payWeek[6][0] == 0:
            self.payWeek[6][1] = self.payWeek[6][1] - 1
            if self.payWeek[6][1] == 0:
                self.payWeek[6][1] = 12
                self.payWeek[6][2] = self.payWeek[6][2] - 1
            daysInMonth = calendar.monthrange(self.payWeek[6][2], self.payWeek[6][1])[1]            
            #self.sMonth = self.eMonth
            #self.sYear = self.eYear
            
            for i in range(7):
                self.payWeek[6-i][0] = daysInMonth - i
                self.payWeek[6-i][1] = self.payWeek[6][1]
                self.payWeek[6-i][2] = self.payWeek[6][2]
        else:
            prevDay = self.payWeek[6][0] - 1
            for i in range(5, -1, -1):
                if prevDay > 0:
                    self.payWeek[i][0] = prevDay
                    self.payWeek[i][1] = self.payWeek[6][1]
                    self.payWeek[i][2] = self.payWeek[6][2]
                    prevDay = prevDay - 1
                elif prevDay == 0:
                    self.payWeek[0][1] = self.payWeek[0][1] - 1
                    if self.payWeek[0][1] == 0:
                        self.payWeek[0][1] = 12
                        self.payWeek[0][2] = self.payWeek[0][2] - 1
                    daysInMonth = calendar.monthrange(self.payWeek[0][2], self.payWeek[0][1])[1]                    
                    self.payWeek[i][0] = daysInMonth
                    self.payWeek[i][1] = self.payWeek[0][1]
                    self.payWeek[i][2] = self.payWeek[0][2]
                    prevDay = -1
                else:
                    self.payWeek[i][0] = daysInMonth + prevDay
                    self.payWeek[i][1] = self.payWeek[0][1]
                    self.payWeek[i][2] = self.payWeek[0][2]
                    prevDay = prevDay - 1
                        
                
           
        self.startDate = str(self.payWeek[0][1]) + '/' + str(self.payWeek[0][0]) + '/' + str(self.payWeek[0][2])
        self.endDate = str(self.payWeek[6][1]) + '/' + str(self.payWeek[6][0]) + '/' + str(self.payWeek[6][2])
        self.setPayPeriod()
        self.payPeriodLbl2.configure(text = self.payPeriod)
        

if __name__ == '__main__':
    
    w = Tk()
    calendar.setfirstweekday(6) #need to call this before calling MonthlyCalender()
    
    dayName = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')
    t = PayPeriod(None, dayName)
    print(t.startDate)
    print(t.endDate)
    #print(t.currentPayPeriod())
    #t.payPeriodGui()
    mainloop()
    