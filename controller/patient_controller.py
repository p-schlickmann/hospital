from datetime import datetime, timedelta
from random import randint

from controller.base_controller import BaseController
from data.patient_dao import PatientDAO
from model.illness import Illness
from model.patient import Patient
from view.patient_view import PatientView


class PatientController(BaseController):
    def __init__(self, system_controller):
        self.__patients_line = []
        self.__system_controller = system_controller
        self.__view = PatientView()
        self.__dao = PatientDAO('data/patients.pkl', Patient)
        super().__init__(self.__view, self.__system_controller)

    def find_patient_by_cpf(self, cpf, display_not_found_msg=False, not_discharged=False, history=False):
        """
        Searches for patient with the given cpf
        :return: list of Patients instances if found, otherwise None
        """
        admittions_list = self.__dao.get(cpf)
        if not admittions_list:
            if display_not_found_msg:
                self.__view.display_msg(f'Nenhum paciente foi encontrado com esse CPF ({cpf}).\n'
                                        f'Verifique se o cpf é valido e foi digitado apenas com números.',
                                        success=False)
            return
        *_, last_time_in_hospital = admittions_list
        if not_discharged and last_time_in_hospital.discharged_at:
            self.__view.display_msg(f'O paciente de CPF {cpf} já recebeu alta!', success=False)
            return
        return admittions_list if history else last_time_in_hospital

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
        info = self.__view.ask_for_main_info()
        if info:
            name, phone, emergency_contact, birth = info
            arrived_at, admitted_at = self.get_arrival_and_admittion_datetime()
            return Patient(name, phone, cpf, birth, emergency_contact, arrived_at, admitted_at)

    def diagnose(self):
        try:
            patient = self.__patients_line[0]['patient']
        except IndexError:
            self.__view.display_msg('Nenhum paciente na fila!', success=False)
            return
        symptom = self.__view.enter_symptom(patient)
        if symptom:
            name, desc, discomfort_level = symptom
            patient.add_symptom(name, desc, discomfort_level)
            illness = self.__view.enter_illness(patient)
            if illness:
                name, desc, severity = illness
                created_illness = Illness(name, desc, severity)
                patient.add_illness(created_illness)
                health_status = self.__view.get_health_status(patient)
                if health_status:
                    patient.health_status = health_status

                    patient_cpf = patient.cpf
                    self.__patients_line = [patient for patient in self.__patients_line if patient['patient'].cpf != patient_cpf]
                    cpfs = self.__view.get_doctors_that_diagnosed_the_patient()
                    for cpf in cpfs:
                        if cpf:
                            doc = self.__system_controller.doc_controller.find_doctor_by_cpf(cpf, display_not_found_msg=False)
                            if doc:
                                patient.add_doctor(doc)

                    self.__view.display_msg('Paciente atendido com sucesso!', success=True)
            patient.diagnosed_at = datetime.now()
        self.__dao.edit_current_patient(patient.cpf, patient)
        self.__system_controller.open_patient_view()

    def admit_patient(self):
        cpf = self.__view.ask_for_cpf()
        if cpf:
            patient = self.find_patient_by_cpf(cpf)
            if patient is None:
                new_patient = self.ask_for_patient_info_and_create_patient(cpf)
            else:
                if not patient.discharged_at:
                    self.__view.display_msg('Esse paciente já foi admitido! ', success=False)
                    return
                use_this_registry = self.__view.use_this_registry(patient)
                if use_this_registry:
                    arrived_at, admitted_at = self.get_arrival_and_admittion_datetime()
                    new_patient = Patient(
                        patient.name, patient.phone_number, patient.cpf,
                        patient.date_of_birth, patient.emergency_contact,
                        arrived_at, admitted_at
                    )
                else:
                    new_patient = self.ask_for_patient_info_and_create_patient(patient.cpf)
            if new_patient:
                if patient:
                    admittions_list = self.find_patient_by_cpf(patient.cpf, history=True) + [new_patient]
                else:
                    admittions_list = [new_patient]
                self.__dao.add(new_patient.cpf, admittions_list, force_insert=True)
                self.add_patient_to_line(new_patient, randint(0, 5))
                self.__view.display_msg('Paciente admitido com sucesso!', success=True)
        self.__system_controller.open_patient_view()

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
        cpf = self.__view.ask_for_cpf()
        if cpf:
            patient = self.find_patient_by_cpf(cpf, display_not_found_msg=True, not_discharged=True)
            if patient is not None:
                if not patient.diagnosed_at:
                    self.__view.display_msg('Esse paciente ainda não foi atendido!', success=False)
                else:
                    if self.__view.confirm_patient_discharge(patient):
                        patient_to_discharge_cpf = patient.cpf
                        self.__patients_line = [
                            patient for patient in self.__patients_line if patient['patient'].cpf != patient_to_discharge_cpf
                        ]
                        patient.discharged_at = datetime.now()
                        self.__dao.edit_current_patient(patient.cpf, patient)
                        self.__view.display_msg(f'{patient.name} recebeu alta!', success=True)
        self.__system_controller.open_patient_view()

    def get_patient_history_and_data(self):
        cpf = self.__view.ask_for_cpf()
        if cpf:
            previous_admittions = self.find_patient_by_cpf(cpf, display_not_found_msg=True, history=True)
            if previous_admittions:
                self.__view.display_patient_history(previous_admittions)
        self.__system_controller.open_patient_view()

    def delete_patient(self):
        """
        Deletes patient by cpf
        :return:
        """
        cpf = self.__view.ask_for_cpf()
        if cpf:
            patient = self.find_patient_by_cpf(cpf, display_not_found_msg=True)
            if patient is not None:
                if self.__view.confirm_patient_deletion(patient):
                    self.__patients_line = [patient for patient in self.__patients_line if patient['patient'].cpf != cpf]
                    self.__dao.remove(patient.cpf)
                    self.__view.display_msg('Dados e histórico do paciente excluídos com sucesso!', success=True)
        self.__system_controller.open_patient_view()

    def get_patient_line(self):
        self.__view.show_waiting_line(self.__patients_line)
        self.__system_controller.open_patient_view()

    def update_health_status(self):
        cpf = self.__view.ask_for_cpf()
        if cpf:
            patient = self.find_patient_by_cpf(cpf, display_not_found_msg=True, not_discharged=True)
            if patient is not None:
                new_status = self.__view.get_health_status(patient)
                if new_status:
                    patient.health_status = new_status
                    self.__dao.edit_current_patient(patient.cpf, patient)
                    self.__view.display_msg('Estado de saúde do paciente atualizado com sucesso!', True)
        self.__system_controller.open_patient_view()
