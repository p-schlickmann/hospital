from datetime import datetime, timedelta
from random import randint

from controller.base_controller import BaseController
from model.illness import Illness
from model.patient import Patient
from view.patient_view import PatientView


class PatientController(BaseController):
    def __init__(self, system_controller):
        self.__patients = []
        self.__patients_line = []
        self.__system_controller = system_controller
        self.__view = PatientView()
        super().__init__(self.__view, self.__system_controller)

    def find_patient_by_cpf(self, cpf, display_not_found_msg=False, not_discharged=False):
        """
        Searches for patient with the given cpf
        :return: Patient if found, otherwise None
        """
        if not_discharged:
            patients_found = [
                patient for patient in self.__patients
                if patient.cpf == cpf and not patient.discharged_at
            ]
        else:
            patients_found = [
                patient for patient in self.__patients if patient.cpf == cpf
            ]
        if not patients_found:
            if display_not_found_msg:
                self.__view.display_msg(f'[-] Nenhum paciente foi encontrado com esse CPF ({cpf}).')
                self.__view.display_msg('[!] Verifique se o cpf é valido e foi digitado apenas com números.')
        else:
            return patients_found[0]

    @staticmethod
    def get_arrival_and_admittion_datetime():
        """
        Arrived_at varies from 1 to 15 minutes from now
        :return: arrival and admittion datetimes
        """
        admitted_at = datetime.now()
        arrived_at = admitted_at - timedelta(minutes=randint(1, 15))
        return arrived_at, admitted_at

    def ask_for_patient_info_and_create_patient(self, cpf):
        """
        Asks for patient info and creates the patient
        :param cpf: person cpf
        :return: created patient
        """
        name, phone, birth = self.__view.ask_for_main_info()
        emergency_contact = self.__view.ask_for_emergency_contact()
        arrived_at, admitted_at = self.get_arrival_and_admittion_datetime()
        return Patient(name, phone, cpf, birth, emergency_contact, arrived_at, admitted_at)

    def diagnose(self):
        menu_name = 'Atender paciente da fila'
        self.__view.display_header(menu_name)
        try:
            patient = self.__patients_line[0]['patient']
        except IndexError:
            self.__view.display_msg('[-] Nenhum paciente na fila!')
            return
        self.__view.display_msg(f'Atendendo o paciente {patient}')
        for symptom in self.__view.enter_symptoms():
            patient.add_symptom(symptom['name'], symptom['description'], symptom['discomfort_level'])
        for illness in self.__view.enter_illnesses():
            created_illness = Illness(illness['name'], illness['description'], illness['severity'])
            patient.add_illness(created_illness)
        patient.health_status = self.__view.get_health_status(patient)
        patient_cpf = patient.cpf
        self.__patients_line = [patient for patient in self.__patients_line if patient['patient'].cpf != patient_cpf]
        cpfs = self.__view.get_doctors_that_diagnosed_the_patient()
        for cpf in cpfs:
            if cpf:
                doc = self.__system_controller.doc_controller.find_doctor_by_cpf(cpf, display_not_found_msg=False)
                if doc:
                    patient.add_doctor(doc)

    def admit_patient(self):
        self.__view.display_header('Admitir paciente')
        cpf = self.__view.ask_for_cpf()
        patient = self.find_patient_by_cpf(cpf)
        if patient is None:
            new_patient = self.ask_for_patient_info_and_create_patient(cpf)
        else:
            if not patient.discharged_at:
                self.__view.display_msg('[!] Esse paciente já foi admitido! ')
                return
            self.__view.display_msg('[+] Encontramos um cadastro previamente preenchido para esse paciente:')
            self.__view.display_person_info(patient, only_base_info=True)
            use_this_registry = self.__view.use_this_registry()
            if use_this_registry:
                arrived_at, admitted_at = self.get_arrival_and_admittion_datetime()
                new_patient = Patient(
                    patient.name, patient.phone_number, patient.cpf,
                    patient.date_of_birth, patient.emergency_contact,
                    arrived_at, admitted_at
                )
            else:
                new_patient = self.ask_for_patient_info_and_create_patient(patient.cpf)
        self.__patients.append(new_patient)
        self.add_patient_to_line(new_patient, randint(0, 5))
        self.__view.display_msg('[+] Paciente admitido com sucesso!')

    def add_patient_to_line(self, patient, illness_severity):
        """
        Adds patient to patient line based on illness severity, that can vary from 0 to 5.
        Patient arrival time is used as a tie breaker
        :param patient: Patient instance
        :param illness_severity: random integer between 0 to 5
        :return: None
        """
        line = self.__patients_line
        delta = datetime.now() - patient.arrived_at
        patient_to_be_appended = {'patient': patient, 'severity': illness_severity, 'delta': delta}
        line.append(patient_to_be_appended)
        line.sort(key=lambda x: (x['severity'], x['delta']), reverse=True)
        self.__patients_line = line

    def discharge_patient(self):
        self.__view.display_header('Dar alta para um paciente')
        cpf = self.__view.ask_for_cpf()
        patient = self.find_patient_by_cpf(cpf, display_not_found_msg=True, not_discharged=True)
        if patient is not None:
            self.__view.display_person_info(patient)
            if self.__view.confirm_action('Dar alta para o paciente encontrado?'):
                patient.discharged_at = datetime.now()
                self.__view.display_msg(f'[+] {patient.name} recebeu alta!')

    def get_patient_history_and_data(self):
        self.__view.display_header('Ver dados/histórico de um paciente')
        cpf = self.__view.ask_for_cpf()
        patient = self.find_patient_by_cpf(cpf, display_not_found_msg=True)
        if patient is not None:
            previous_admittions = [patient for patient in self.__patients if patient.cpf == cpf]
            self.__view.display_patient_history(previous_admittions)

    def delete_patient(self):
        """
        Deletes patient by cpf
        :return:
        """
        self.__view.display_header("Excluir paciente")
        cpf = self.__view.ask_for_cpf()
        patient = self.find_patient_by_cpf(cpf, display_not_found_msg=True)
        if patient is not None:
            self.__view.display_person_info(patient, only_base_info=True)
            confirmed = self.__view.confirm_action('Deletar todas as informações do paciente selecionado?')
            if confirmed:
                self.__patients_line = [patient for patient in self.__patients_line if patient['patient'].cpf != cpf]
                self.__patients = [patient for patient in self.__patients if patient.cpf != cpf]
                self.__view.display_msg('[+] Dados e histórico do paciente excluídos com sucesso!')

    def get_patient_line(self):
        self.__view.display_header('Ver fila de atendimento')
        self.__view.show_waiting_line(self.__patients_line)

    def update_health_status(self):
        self.__view.display_header('Atualizar estado de saúde de um paciente')
        cpf = self.__view.ask_for_cpf()
        patient = self.find_patient_by_cpf(cpf, display_not_found_msg=True, not_discharged=True)
        if patient is not None:
            new_status = self.__view.get_health_status(patient)
            if new_status:
                patient.health_status = new_status
                self.__view.display_msg('[+] Estado de saúde do paciente atualizado com sucesso!')
