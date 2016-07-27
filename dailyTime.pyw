from decimal import Decimal

class DailyTime:
    
    def __init__(self, timeInHour, timeInMinute, inAm, timeOutHour, timeOutMinute, outPm):
        #getcontext().prec = 4
        self.timeInHour = timeInHour         #integer value
        self.timeOutHour = timeOutHour       #integer    
        self.timeInMinute = timeInMinute     # in decimal fraction
        self.timeOutMinute = timeOutMinute   # in decimal fraction
        self.inAm = inAm
        self.outPm = outPm
        self.totalHours = self.getWorkedHours()
        #print('total hours: ', self.totalHours)
        
    def getTimeInHour(self):
        return self.timeInHour
        
    def getTimeInMinute(self):
        return self.timeInMinute  #
    
    def getTimeOutHour(self):
        return self.timeOutHour
        
    def getTimeOutMinute(self):
        return self.timeOutMinute  # 

    def setTimeInHour(self, hour):
        self.timeInHour = hour
    def setTimeInMinute(self, minute):
        self.timeInMinute = minute
    def setTimeOutHour(self, hour):
        self.timeOutHour = hour
    def setTimeOutMinute(self, minute):
        self.timeOutMinute = minute
        
    def getWorkedHours(self):
        #getcontext().prec = 4
        if self.inAm == 1:
            if self.timeInHour != 12:
                timeInHour = self.timeInHour
            else:
                timeInHour = 0
        else:
            if self.timeInHour != 12:
                timeInHour = self.timeInHour + 12
            else:
                timeInHour = 12
                
        if self.outPm == 2:
            if self.timeOutHour != 12:
                timeOutHour = self.timeOutHour + 12
            else:
                timeOutHour = 12
        else:
            if self.timeOutHour != 12:
                timeOutHour = self.timeOutHour
            else:
                timeOutHour = 0
        
        totalTimeInMinute = timeInHour * Decimal ('60') + int(self.timeInMinute * Decimal('100'))
        totalTimeOutMinute = timeOutHour * Decimal ('60') + int(self.timeOutMinute * Decimal('100'))
        totalHours = ((totalTimeOutMinute - totalTimeInMinute) / Decimal('60')).quantize(Decimal('.01'))        
        '''print('totalTimeInMinute: ', totalTimeInMinute)
        print('totalTimeOutMinute: ', totalTimeOutMinute)
        print(self.timeInMinute, " ", self.timeOutMinute)
        '''
        
        return totalHours #Need to be Decimal object
               
            
           
