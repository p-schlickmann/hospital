from datetime import datetime

from controller.base_controller import BaseController
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
            raise SystemError(f'Dois pacientes foram encontrados com o mesmo cpf {patients_found}.')
        elif not patients_found and display_not_found_msg:
            self.__view.display_msg(f'[-] Nenhum paciente foi encontrado com esse CPF ({cpf}).')
            self.__view.display_msg('[!] Verifique se o cpf é valido e foi digitado apenas com números.')
        else:
            return patients_found[0]

    def ask_for_patient_info_and_create_patient(self, cpf):
        name, phone, birth = self.__view.ask_for_main_info()
        emergency_contact = self.__view.ask_for_emergency_contact()
        admitted_at = datetime.now()
        return Patient(name, phone, cpf, birth, emergency_contact, admitted_at)

    def diagnose(self, patient):
        ''

    def admit_patient(self):
        menu_name = 'Admitir paciente'
        try:
            cpf = self.__view.ask_for_cpf(menu_name)
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
                new_patient = Patient(
                    patient.name, patient.phone_number, patient.cpf,
                    patient.date_of_birth, patient.emergency_contact, datetime.now()
                )
            else:
                new_patient = self.ask_for_patient_info_and_create_patient(patient.cpf)
        self.__patients.append(new_patient)
        self.diagnose(new_patient)
        self.add_patient_to_line(new_patient)

    def add_patient_to_line(self, patient):
        pass

    def discharge_patient(self):
        menu_name = 'dar alta paciente'
        cpf = self.__view.ask_for_cpf(menu_name)

    def get_patient_history_and_data(self):
        menu_name = 'buscar paciente'
        cpf = self.__view.ask_for_cpf(menu_name)

    def delete_patient(self):
        """
        Deletes patient by cpf
        :return:
        """
        menu_name = "-------- Excluir patient ----------"
        cpf = self.__view.ask_for_cpf(menu_name)
        patient = self.find_patient_by_cpf(cpf)

    def get_patient_line(self):
        return []

    def update_health_status(self):
        menu_name = 'atualizar paciente'
        cpf = self.__view.ask_for_cpf(menu_name)
        patient = self.find_patient_by_cpf(cpf)
        self.__view.update_health_status(patient)
