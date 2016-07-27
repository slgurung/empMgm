from decimal import Decimal

#following constants affects overtime rates. When these changes, OT rate also nedd to change automatic
minimumWage = Decimal('9') #when this change, need to update all object of this class**********
overTimeFactor = Decimal('1.5') # same here

class Employee:
    
    def __init__(self, empId, name, street = '', city = '', state = '', zipCode = '',
                 phone = '', payRate = 0, hireDate = '', status = 'active'):
        self.empId = empId
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.phone = phone
        self.payRate = payRate #Decimal(payRate).quantize(Decimal('.01'))
        #self.overTimeRate = self.getOTRate() # This approch doesn't update automatic
        self.hireDate = hireDate
        self.status = status
        
    def getName(self):
        return self.name
    def getId(self):
        return self.empId
    def getStreet(self):
        return self.street
    def getCity(self):
        return self.city
    def getState(self):
        return self.state
    def getZipcode(self):
        return self.zipCode
    def getPhone(self):
        return self.phone
    def getPayRate(self):
        return self.payRate
    def getHireDate(self):
        return self.hireDate
    def getStatus(self):
        return self.status
        
    def getOTRate(self):
        if (self.payRate < minimumWage):
            return ((minimumWage * overTimeFactor) - (minimumWage - self.payRate)).quantize(Decimal('.01'))
        else:
            return (self.payRate * overTimeFactor).quantize(Decimal('.01'))            
        
    
    def setName(self, n):
        self.name = n
    def setId(self, num):
        self.empId = num
    def setStreet(self, st):
        self.street = st
    def setCity(self, c):
        self.city = c
    def setState(self, s):
        self.state = s
    def setZipcode(self, z):
        self.zipCode = z
    def setPhone(self, p):
        self.phone = p
    def setPayRate(self, pay):
        self.payRate = pay
    
           
    
if __name__ == '__main__':  # self test code
    bob = Employee(1, 'Bob Smith')
    sue = Employee(2, 'Sue Jones')
    print (bob.getName(), bob.getId(), sep = ' ** ')
    
   
    
