from controller.base_controller import BaseController
from view.doctor_view import DoctorView


class DoctorController(BaseController):
    def __init__(self, system_controller):
        self.__doctors = []
        self.__system_controller = system_controller
        self.__view = DoctorView()
        super().__init__(self.__view)

    def find_doctor_by_cpf(self, cpf):
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

    def register_doctor(self):
        self.__view.ask_for_cpf('')
        self.__view.display_register_doctor('')

    def edit_doctor(self):
        self.__view.ask_for_cpf('')
        self.__view.display_edit_doctor('')

    def get_doctor(self):
        self.__view.ask_for_cpf('')

    def delete_doctor(self):
        """
        Deletes doctor by cpf
        :return:
        """
        menu_name = "-------- Excluir médico ----------"
        cpf = self.__view.ask_for_cpf(menu_name)
        doc = self.find_doctor_by_cpf(cpf)

    def get_on_call_doctors(self):
        pass

    def call_doctor(self):
        pass