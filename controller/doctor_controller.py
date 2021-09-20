from datetime import datetime

from controller.base_controller import BaseController
from data.data_access_object import DataAccessObject
from model.doctor import Doctor
from view.doctor_view import DoctorView


class DoctorController(BaseController):
    def __init__(self, system_controller):
        self.__system_controller = system_controller
        self.__view = DoctorView()
        self.__dao = DataAccessObject('data/doctors.pkl', Doctor)
        super().__init__(self.__view, self.__system_controller)

    def new_doctor(self):
        doctor_info = self.__view.new_doctor()
        if doctor_info:
            id, title, desc = doctor_info
            if not id or not title:
                self.__view.display_msg('Especifique pelo menos um titulo e um id!', success=False)
            else:
                doctor = Doctor(id, title, desc, datetime.now())
                self.__dao.add(doctor.id, doctor)
                self.__view.display_msg('Médico criado com sucesso!', success=True)
        self.__system_controller.open_doctor_view()

    def find_doctor_by_id(self, id):
        doctor = self.__dao.get(id)
        if doctor:
            return doctor
        else:
            self.__view.display_msg(f'Nenhum médico encontrado com esse id! ({id})', success=False)

    def edit_doctor(self):
        id = self.__view.ask_for_doctor_id()
        if id:
            doctor = self.find_doctor_by_id(id)
            if doctor is not None:
                edit_doctor_info = self.__view.edit_doctor(doctor)
                if edit_doctor_info:
                    title, desc = edit_doctor_info
                    if title:
                        doctor.title = title
                    if desc:
                        doctor.description = desc
                    self.__dao.add(doctor.id, doctor)
                    self.__view.display_msg('Médico editado com sucesso!', success=True)
        self.__system_controller.open_doctor_view()

    def delete_doctor(self):
        id = self.__view.ask_for_doctor_id()
        if id:
            doctor_to_remove = self.find_doctor_by_id(id)
            if doctor_to_remove is not None:
                confirmed = self.__view.confirm_doctor_deletion(doctor_to_remove)
                if confirmed:
                    self.__dao.remove(doctor_to_remove.id)
                    self.__view.display_msg('Médico excluído com sucesso!', success=True)
        self.__system_controller.open_doctor_view()

    def list_doctors(self):
        doctors = self.__dao.get_all()
        self.__view.list_doctors(doctors)
        self.__system_controller.open_doctor_view()
