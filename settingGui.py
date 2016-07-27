# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 10:17:39 2016

@author: mars
"""
from tkinter import *
import shelve
import calendar

class SettingGui:
    def __init__(self, parent = None):
        self.parent = parent
        #self.firstDay = 5
        #self.weekDayOrder = []
        
        self.settingDB = shelve.open('setting/' + 'settingFile')
        if self.settingDB:
            self.firstDay = self.settingDB['firstDay'] 
            self.weekDayOrder = self.settingDB['weekDayOrder']
            print('no first time')
        else:            
            self.firstDay = 5
            self.weekDayOrder = []
            self.settingDB['firstDay'] = self.firstDay
            self.settingDB['weekDayOrder'] = self.weekDayOrder
            print('first time')
            
        self.setWeeklyDay(self.firstDay)
        self.settingDB.close()
    
        
    def setWeeklyDay(self, fDay):
        if not self.weekDayOrder:
            calendar.setfirstweekday(fDay) #6 is sunday, can do like,calendar.setfirstweekday(calendar.SUNDAY)
            calObj = calendar.Calendar(calendar.firstweekday()) #cal object with firstDay as first day of week
        
            iterWeek = calObj.iterweekdays()
            #self.weekDayOrder = []
            for dayNum in iterWeek: #sets days of week according to first day of week setting
                self.weekDayOrder.append(calendar.day_abbr[dayNum])
                
            self.settingDB['weekDayOrder'] = self.weekDayOrder
            print('hello')
        print(self.weekDayOrder)
        
    
    
if __name__ == '__main__':
   
    c = SettingGui()
    
