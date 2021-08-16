from model.person import Person


class Patient(Person):
    def __init__(self, name: str, phone_number: int, cpf: int, date_of_birth: datetime, emergency_contact: int, arrived_at: datetime, admitted_at: datetime, discharged_at: datetime):
        self.__name = name
        self.__phone_number = phone_number
        self.__cpf = cpf
        self.__date_of_birth = date_of_birth
        self.__emergency_contact = emergency_contact
        self.__arrived_at = arrived_at
        self.__admitted_at = admitted_at
        
    @property
    def emergency_contact(self):
        return self.__emergency_contact
    
    @emergency_contact.setter
    def emergency_contact(self, emergency_contact:int):
        self.__emergency_contact = emergency_contact
        
    @property
    def arrived_at(self):
        return self.__arrived_at
    
    @arrived_at.setter
    def arrived_at(self, arrived_at: datetime):
        self.__arrived_at = arrived_at
        
    @property
    def admitted_at(self):
        return self.__admitted_at
    
    @admitted_at.setter
    def admitted_at(self, admitted_at: int):
        self.__admitted_at = admitted_at
        
    @property
    def discharged_at(self):
        return self.__discharged_at
    
    @discharged_at.setter
    def discharged_at(self):
        self.__discharged_at = discharged_at
        
