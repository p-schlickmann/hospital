from controller.base_controller import BaseController
from view.patient_view import PatientView


class PatientController(BaseController):
    def __init__(self, system_controller):
        self.__patients = []
        self.__patients_line = []
        self.__system_controller = system_controller
        self.__view = PatientView()
        super().__init__(self.__view, self.__system_controller)

    def find_patient_by_cpf(self, cpf):
        """
        Searches for patient with the given cpf
        :return: Patient if found, otherwise None
        """
        return ''

    def admit_patient(self):
        menu_name = 'amitir paciente'
        cpf = self.__view.ask_for_cpf(menu_name)

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
