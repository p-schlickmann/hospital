from abc import ABC, abstractmethod
from datetime import datetime


class Person(ABC):
    @abstractmethod
    def __init__(self, name: str, phone_number: str, cpf: str, date_of_birth: datetime):
        self.__name = name
        self.__phone_number = phone_number
        self.__cpf = cpf
        self.__date_of_birth = date_of_birth
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name
        
    @property
    def phone_number(self):
        return self.__phone_number
    
    @phone_number.setter
    def phone_number(self, phone_number: str):
        self.__phone_number = phone_number
        
    @property
    def cpf(self):
        return self.__cpf
    
    @cpf.setter
    def cpf(self, cpf: str):
        self.__cpf = cpf
        
    @property
    def date_of_birth(self):
        return self.__date_of_birth
    
    @date_of_birth.setter
    def date_of_birth(self, date_of_birth: datetime):
        self.__date_of_birth = date_of_birth
