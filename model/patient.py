from model.person import Person
from doctor import Doctor
from illness import Illness
from synptom import Symptoms


class Patient(Person):
    def __init__(self, name: str, phone_number: int, cpf: int, date_of_birth: datetime, emergency_contact: int, arrived_at: datetime, admitted_at: datetime, discharged_at: datetime):
        self.__name = name
        self.__phone_number = phone_number
        self.__cpf = cpf
        self.__date_of_birth = date_of_birth
        self.__emergency_contact = emergency_contact
        self.__arrived_at = arrived_at
        self.__admitted_at = admitted_at
        self.__doctors = []
        self.__illnesses = []
        self.__symptoms = []
        
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
        
    def add_doctor(self, doctor: Doctor):
        if (doctor is not None) and (isinstance(doctor, Doctor)):
            if doctor not in self.__doctors:
                self.__doctors.append(doctor)
                
    def remove_doctor(self, doctor: Doctor):
        if (doctor is not None) and (isinstance(doctor, Doctor)):
            if doctor in self.__doctors:
                self.__remove(doctor)
                
    def add_illness(self, illness: Illness):
        if (illness is not None) and (isinstance(illness, Illness)):
            if illness not in self.__illnesses:
                self.__illnesses.append(illness)
                
    def remove_illness(self, illness: Ilness):
        if (illness is not None) and (isinstance(illness, Illness)):
            if illness in self.__illnesses:
                self.__remove(illness)
                
    def add_symptom(self, sympton.name, sympton.description, symptom.discomfort_level):
        if (symptom is not None) and (isinstance(symptom, Symptom)):
            if symptom not in self.__symptoms:
                self.__symptoms.append(symptom)
                
    def remove_symptom(self, sympton.id):
        if (symptom is not None) and (isinstance(symptom, Symptom)):
            if symptom in self.__symptom:
                self.__remove(symptom)
