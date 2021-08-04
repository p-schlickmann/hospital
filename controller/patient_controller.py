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

    def find_patient_by_cpf(self, cpf, display_not_found_msg=False):
        """
        Searches for patient with the given cpf
        :return: Patient if found, otherwise None
        """
        patients_found = [patient for patient in self.__patients if patient.cpf == cpf]
        if len(patients_found) > 1:
            self.__view.display_msg(f'[!] Erro no sistema! Dois pacientes foram encontrados com o mesmo cpf {patients_found}.')
            raise SystemError
        elif not patients_found and display_not_found_msg:
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
        for symptom in self.__view.enter_symptoms():
            patient.add_symptom(symptom['name'], symptom['description'], symptom['discomfort_level'])
        for illness in self.__view.enter_illnesses():
            created_illness = Illness(illness['name'], illness['description'], illness['severity'])
            patient.add_illness(created_illness)

    def admit_patient(self):
        menu_name = 'Admitir paciente'
        cpf = self.__view.ask_for_cpf(menu_name)
        try:
            patient = self.find_patient_by_cpf(cpf)
        except SystemError:
            return
        if patient is None:
            new_patient = self.ask_for_patient_info_and_create_patient(cpf)
        else:
            self.__view.display_msg('[+] Encontramos um cadastro previamente preenchido para esse paciente:')
            self.__view.display_person_info(patient)
            use_this_registry = self.__view.use_this_registry()
            if use_this_registry:
                arrived_at, admitted_at = self.get_arrival_and_admittion_datetime()
                new_patient = Patient(
                    patient.name, patient.phone_number, patient.cpf,
                    patient.date_of_birth, patient.emergency_contact, arrived_at, admitted_at
                )
            else:
                new_patient = self.ask_for_patient_info_and_create_patient(patient.cpf)
        self.__patients.append(new_patient)
        self.add_patient_to_line(new_patient, randint(0, 5))

    def add_patient_to_line(self, patient, illness_severity):
        """
        Adds patient to patient line based on illness severity, that can vary from 0 to 5.
        Patient arrival time is used as a tie breaker
        :param patient: Patient instance
        :param illness_severity: random integer between 0 to 5
        :return: None
        """
        line = self.__patients_line
        patient_to_be_appended = {'patient': patient, 'severity': illness_severity}
        if not line:
            self.__patients_line.append(patient_to_be_appended)
        else:
            first_patient = line[0]
            if first_patient['severity'] < illness_severity:
                self.__patients_line = [patient_to_be_appended] + line
            else:
                indexes_of_patients_with_the_same_severity = [
                    index for index, patient in enumerate(line) if patient['severity'] == illness_severity
                ]
                if not indexes_of_patients_with_the_same_severity:
                    # find the first patient in line that has a lower severity then passed patient
                    try:
                        index_of_the_first_patient_with_less_severity = [
                            index for index, patient in enumerate(line) if patient['severity'] < illness_severity
                        ][0]
                        cutting_point = index_of_the_first_patient_with_less_severity - 1
                        self.__patients_line = line[0:cutting_point] + [patient_to_be_appended] + line[cutting_point:]
                    except IndexError:
                        self.__patients_line.append(patient_to_be_appended)
                else:
                    # tie break based on arrival time
                    for patient_index in indexes_of_patients_with_the_same_severity:
                        found_patient = line[patient_index]
                        if found_patient['patient'].arrived_at < patient.arrived_at:
                            # if found patient arrived earlier then we did,
                            # check if the next patient with the same severity arrived after we did
                            # if both are true, append the patient between them
                            try:
                                next_patient_in_line = line[patient_index + 1]
                                if next_patient_in_line['severity'] != illness_severity:
                                    raise IndexError
                            except IndexError:
                                # there was no patient with the same severity further down the line,
                                # so we can append this new patient right after this last one
                                cutting_point = patient_index + 1
                                self.__patients_line = line[0:cutting_point] + [patient_to_be_appended] + line[cutting_point:]
                                break
                            else:
                                # there was a next patient in line with the same severity
                                # now if this patient arrived after this one, we should append this one before him.
                                if next_patient_in_line['patient'].arrived_at > patient.arrived_at:
                                    cutting_point = patient_index + 1
                                    self.__patients_line = line[0:cutting_point] + [patient_to_be_appended] + line[cutting_point:]
                                    break

    def discharge_patient(self):
        menu_name = 'Dar alta para um paciente'
        cpf = self.__view.ask_for_cpf(menu_name)
        try:
            patient = self.find_patient_by_cpf(cpf, display_not_found_msg=True)
        except SystemError:
            return
        if patient is not None:
            self.__view.display_person_info(patient)
            if self.__view.confirm_discharge():
                patient.discharged_at = datetime.now()
                self.__view.display_msg(f'[+] {patient.name} recebeu alta!')

    def get_patient_history_and_data(self):
        menu_name = 'Ver dados/histórico de um paciente'
        cpf = self.__view.ask_for_cpf(menu_name)
        try:
            patient = self.find_patient_by_cpf(cpf, display_not_found_msg=True)
        except SystemError:
            return
        if patient is not None:
            previous_admittions = [patient for patient in self.__patients if patient.cpf == cpf]
            self.__view.display_patient_history(previous_admittions)

    def delete_patient(self):
        """
        Deletes patient by cpf
        :return:
        """
        menu_name = "Excluir paciente"
        cpf = self.__view.ask_for_cpf(menu_name)
        patient = self.find_patient_by_cpf(cpf)

    def get_patient_line(self):
        return []

    def update_health_status(self):
        menu_name = 'atualizar paciente'
        cpf = self.__view.ask_for_cpf(menu_name)
        patient = self.find_patient_by_cpf(cpf)
        self.__view.update_health_status(patient)
