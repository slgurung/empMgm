from tkinter import *
import calendar
from datetime import date
#import datetime

#weekDayOrder = []
#firstDay = 5; #By 0 is monday, and 6 is Sunday; make this setup at setting

class MonthlyCalender:
    def __init__(self, parent = None, dayOrder = ''):
        self.parent = parent       
        self.calenderFrame = Frame(self.parent, width = 364, height = 350)
        self.calenderFrame.pack()
        
        self.dayButton = [[0] * 7 for i in range(6)]
        self.year = 0 
        self.month = 0
        self.day = 0
        
        self.makeCalendar(dayOrder)
        
    
    def makeCalendar(self, dayOrder):
        #global dayButton #**maybe change to self.global at __init__
        #dayButton = [[0] * 7 for i in range(6)]
        
        d = date.today()
        d = d.timetuple()
        
        self.year = d[0] 
        self.month = d[1]
        self.day = d[2]
        #todayIs = d[6]
        
        
        monthCal = calendar.monthcalendar(self.year, self.month)
        
        row1 = Frame(self.calenderFrame, width = 364, height = 40)
        row1.propagate(0)
        row1.pack(anchor = W)
        self.calendarLabel = Label(row1, text = calendar.month_name[self.month] +', ' + str(self.year) + '   ',
                              font = ('arial', 12, 'bold'))
        self.calendarLabel.pack(side = LEFT)
        previous = Button(row1, text = ' Next >>' , command = self.nextMonth, width = 10, height = 2)
        previous.pack(side = RIGHT)
        previous = Button(row1, text = '<< Previous', command = self.previousMonth, width = 10, height = 2)
        previous.pack(side = RIGHT)        
        
        for i in range(len(dayOrder)):
            row1 = Frame(self.calenderFrame)
            row1.pack(side = LEFT, anchor = N)
            day = Label(row1, text = dayOrder[i] , bd = 2, relief = RIDGE, width = 6, height = 2) 
            day.pack(fill = X)  #could also use calendar.day_name[] or calendar.day_abbr[] instead of dayOrder
            for j in range (6):
                if len(monthCal) > j:
                    day = Button(row1, text = monthCal[j][i]  if monthCal[j][i] else '',
                                 command = lambda row = j, col = i : self.getDay(row, col), width = 6, height = 2)
                    day.pack()
                    if not monthCal[j][i]:
                        day.configure(state = DISABLED)
                else:
                    day = Button(row1, state = DISABLED, width = 6, height = 2,
                                 command = lambda row = j, col = i : self.getDay(row, col))
                    day.pack_forget()
                self.dayButton[j][i] = day
                
    def getDay(self, row, col):
        return (self.dayButton[row][col].cget('text'))
        
                
    def nextMonth(self):
        self.month = self.month + 1
        if self.month == 13:
            self.month = 1
            self.year = self.year + 1
        self.calendarLabel.configure(text = calendar.month_name[self.month] +', ' + str(self.year) + '   ')
       
        monthCal = calendar.monthcalendar(self.year, self.month) 
        for i in range(len(calendar.day_abbr)):
            for j in range (6):
                if len(monthCal) > j:
                    self.dayButton[j][i].configure(text = monthCal[j][i], state = NORMAL)
                    self.dayButton[j][i].pack()
                    if not monthCal[j][i]:
                        self.dayButton[j][i].configure(state = DISABLED, text = '')
                else:
                    self.dayButton[j][i].pack_forget() #.configure(state = DISABLED, bd = 0)

    def previousMonth(self):
        self.month = self.month - 1
        if self.month == 0:
            self.month = 12
            self.year = self.year - 1
        self.calendarLabel.configure(text = calendar.month_name[self.month] +', ' + str(self.year) + '   ')
        
        monthCal = calendar.monthcalendar(self.year, self.month) 
        for i in range(len(calendar.day_abbr)):
            for j in range (6):
                if len(monthCal) > j:
                    self.dayButton[j][i].configure(text = monthCal[j][i], state = NORMAL)
                    self.dayButton[j][i].pack()
                    if not monthCal[j][i]:
                        self.dayButton[j][i].configure(state = DISABLED, text = '')
                else:
                    self.dayButton[j][i].pack_forget() #.configure(state = DISABLED, bd = 0)
        
      
                
                
if __name__ == '__main__':
    w = Tk()
    calendar.setfirstweekday(6)
    dayName = ('Sun  ', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')
    c = MonthlyCalender(None, dayName)
    #c.makeCalendar(dayName)
    mainloop()



'''# ask of month and year
yy = int(input("Enter year: "))
mm = int(input("Enter month: "))

# display the calendar
print(calendar.monthcalendar(yy,mm))
calendar.setfirstweekday(calendar.SATURDAY)
print(calendar.firstweekday())
'''

