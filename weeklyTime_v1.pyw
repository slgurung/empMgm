from dailyTime import DailyTime
from tkinter.messagebox import showinfo
from decimal import Decimal

maxHour = 15
class WeeklyTime:
    def __init__(self):
        self.dailyTimeObj = {}
        self.rate = 0       #this may be usefull to record rate at specific week, as it may change
        self.totalHour = 0 #Decimal obj. This can't initialize to 0.0
        self.regularHour = 0
        self.overTime = 0   #because Decimal and float are not supported
        self.overTimeRate = 0
        self.totalPay = 0   #for math operands, +, * , -, / etc.
                
    def setDailyTime(self, day, tInH, tInM, inAm, tOutH, tOutM, outPm ): #tInM and tOutM are in decimal value
        #dailyObj = DailyTime(tInH, tInM, inAm, tOutH, tOutM, outPm)
        if  1 <= tInH <= 12 and 1 <= tOutH <= 12 and 0 <= tInM < 0.60 and 0 <= tOutM < 0.60:
            dailyObj = DailyTime(tInH, tInM, inAm, tOutH, tOutM, outPm)
            if 0 <= dailyObj.totalHours <= maxHour:
                self.dailyTimeObj[day] = dailyObj
            elif dailyObj.totalHours <= 0:
                showinfo('', 'Time-Out is earlier than Time-In. Enter again.')
            else:
                showinfo('', 'Exceed the maximum hours can worked. Check and enter again.')
        else:
            showinfo('', 'One or more time is not correct. Check and enter again.')
        #print(self.dailyTimeObj.keys())
        
    def getWeeklyHour(self):
        tHours = 0
        for day in self.dailyTimeObj:
            tHours = tHours + self.dailyTimeObj[day].totalHours
        return tHours
        
    def getTotalPay(self):
        return ((self.regularHour * self.rate) + (self.overTime * self.overTimeRate)).quantize(Decimal('.01'))

        
if __name__ == '__main__':
    surya = WeeklyTime()
    surya.setDailyTime('sun', 9, Decimal('.30'), 1, 5, Decimal('0.12'), 2)
        
    print('totalHours: ', surya.getWeeklyHour())
   
    
            
            

    
