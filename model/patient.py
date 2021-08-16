from datetime import datetime

from model.person import Person
from model.doctor import Doctor
from model.illness import Illness
from model.symptom import Symptom
from model.health_status import HealthStatus


class Patient(Person):
    def __init__(self, name: str, phone_number: str, cpf: str, date_of_birth: datetime,
                 emergency_contact: str, arrived_at: datetime):
        super().__init__(name, phone_number, cpf, date_of_birth)
        self.__emergency_contact = emergency_contact
        self.__arrived_at = arrived_at
        self.__admitted_at = None
        self.__discharged_at = None
        self.__health_status = None
        self.__doctors = []
        self.__illnesses = []
        self.__symptoms = []

    def __str__(self):
        return f'{self.cpf} | {self.name}'

    @property
    def emergency_contact(self):
        return self.__emergency_contact
    
    @emergency_contact.setter
    def emergency_contact(self, emergency_contact: str):
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
    def admitted_at(self, admitted_at: datetime):
        self.__admitted_at = admitted_at
        
    @property
    def discharged_at(self):
        return self.__discharged_at
    
    @discharged_at.setter
    def discharged_at(self, discharged_at: datetime):
        self.__discharged_at = discharged_at
        
    @property
    def health_status(self):
        return self.__health_status
    
    @health_status.setter
    def health_status(self, health_status: HealthStatus):
        self.__health_status = health_status

    @property
    def doctors(self):
        return self.__doctors
        
    def add_doctor(self, doctor: Doctor):
        """
        Adds doctor to doctors list
        :param doctor: Doctor instance
        :return: the added doctor if successful, None otherwise
        """
        if (doctor is not None) and (isinstance(doctor, Doctor)):
            if doctor not in self.__doctors:
                self.__doctors.append(doctor)
                return doctor
                
    def remove_doctor(self, doctor: Doctor):
        """
        Removes doctor from doctors list
        :param doctor: Doctor instance
        :return: True if successful, False otherwise
        """
        if (doctor is not None) and (isinstance(doctor, Doctor)):
            if doctor in self.__doctors:
                self.__doctors.remove(doctor)
                return True
        return False

    @property
    def illnesses(self):
        return self.__illnesses

    def add_illness(self, illness: Illness):
        """
        Adds illness to illnesses list
        :param illness: Illness instance
        :return: added illness if successful, otherwise None
        """
        if (illness is not None) and (isinstance(illness, Illness)):
            if illness not in self.__illnesses:
                self.__illnesses.append(illness)
                return illness

    def remove_illness(self, illness: Illness):
        """
        Removes illness from illnesses list
        :param illness: Illness instance
        :return: True if successful, False otherwise
        """
        if (illness is not None) and (isinstance(illness, Illness)):
            if illness in self.__illnesses:
                self.__illnesses.remove(illness)
                return True
        return False

    @property
    def symptoms(self):
        return self.__symptoms

    def symptom_id_available(self, symptom_id):
        return not [symptom for symptom in self.__symptoms if symptom.id == symptom_id]

    def add_symptom(self, name, description, discomfort_level):
        """
        Adds symptom to symptoms list
        Auto increments symptom id
        :return: added symptom if successful, otherwise None
        """
        *_, last_symptom = self.__symptoms
        new_symptom_id = last_symptom.id + 1
        id_available = self.symptom_id_available(new_symptom_id)
        while not id_available:
            new_symptom_id = new_symptom_id + 1
            id_available = self.symptom_id_available(new_symptom_id)
        symptom = Symptom(name, description, discomfort_level, new_symptom_id)
        self.__symptoms.append(symptom)
                
    def remove_symptom(self, symptom_id):
        self.__symptoms = [symptom for symptom in self.__symptoms if symptom.id == symptom_id]
