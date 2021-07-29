from controller.base_controller import BaseController
from view.system_view import SystemView
from controller.doctor_controller import DoctorController
from controller.patient_controller import PatientController


class SystemController(BaseController):

    def __init__(self):
        self.__doctor_controller = DoctorController(self)
        self.__patient_controller = PatientController(self)
        self.__view = SystemView()
        super().__init__(self.__view)

    @staticmethod
    def exit():
        exit(0)

    def open_patient_view(self):
        options = {
            0: self.__patient_controller.return_to_main_menu,
            1: self.__patient_controller.register_patient,
            2: self.__patient_controller.edit_patient,
            3: self.__patient_controller.get_patient,
            4: self.__patient_controller.delete_patient,
            5: self.__patient_controller.get_patient_line,
        }
        self.__patient_controller.open_view(options)

    def open_doctor_view(self):
        options = {
            0: self.__doctor_controller.return_to_main_menu,
            1: self.__doctor_controller.register_doctor,
            2: self.__doctor_controller.edit_doctor,
            3: self.__doctor_controller.get_doctor,
            4: self.__doctor_controller.delete_doctor,
            5: self.__doctor_controller.get_on_call_doctors,
            6: self.__doctor_controller.call_doctor,
        }
        self.__doctor_controller.open_view(options)

    def open_log_view(self):
        pass

    def start_system(self):
        self.open_main_view()

    def open_main_view(self):
        options = {
            0: self.exit,
            1: self.open_patient_view,
            2: self.open_doctor_view,
            3: self.open_log_view,
        }
        self.open_view(options)


