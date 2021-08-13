from model.person import Person


class Doctor(Person):
    def __init__(self, name =  str, phone_number: int, cpf: int, date_of_birth: datetime, salary: int, on_call: bool, available = bool):
        self.__name = name
        self.__phone_number = phone_number
        self.__cpf = cpf
        self.__ date_of_birth
        self.__salary = salary
        self.__on_call = on_call
        self.__available = available
        
    @property
    def salary(self):
        return self.__salary
    
    @salary.setter
    def salary(self, salary: int):
        self.__salary = salary
        
    @property
    def on_call(self):
        return self.__on_call
    
    @on_call.setter
    def on_call(self. on_call: bool):
        self.__on_call = on_call
        
    @property
    def available(self):
        return self.__available
    
    @available.setter
    def available(self, available: bool):
        self.__available = available
