from controller.base_controller import BaseController
from view.pacient_view import PatientView


class PatientController(BaseController):
    def __init__(self, system_controller):
        self.__patients = []
        self.__system_controller = system_controller
        self.__view = PatientView()
        super().__init__(self.__view)

    def find_patient_by_cpf(self, cpf):
        """
        Searches for doctor with the given cpf
        :return: Doctor if found, otherwise None
        """
        return ''

    def return_to_main_menu(self):
        """
        Goes back to the system controller view
        :return: None
        """
        return self.__system_controller.open_main_view()

    def register_patient(self):
        pass

    def edit_patient(self):
        pass

    def get_patient(self):
        pass

    def delete_patient(self):
        """
        Deletes patient by cpf
        :return:
        """
        menu_name = "-------- Excluir médico ----------"
        cpf = self.__view.ask_for_cpf(menu_name)
        patient = self.find_patient_by_cpf(cpf)

    def get_patient_line(self):
        return []
