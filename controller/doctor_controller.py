from datetime import datetime
from random import randint

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

    def find_doctor_by_cpf(self, cpf, display_not_found_msg=True):
        """
        Searches for doctor with the given cpf
        :return: Doctor if found, otherwise None
        """
        doctor_found = self.__dao.get(cpf)
        if not doctor_found:
            if display_not_found_msg:
                self.__view.display_msg(f'Nenhum médico foi encontrado com esse CPF ({cpf}).\nVerifique se o cpf é valido e foi digitado apenas com números.', success=False)
        else:
            return doctor_found

    def register_doctor(self):
        cpf = self.__view.ask_for_cpf()
        if cpf:
            if not self.find_doctor_by_cpf(cpf, display_not_found_msg=False):
                doc_info = self.__view.new_doctor()
                if doc_info:
                    name, phone, birth, salary = doc_info
                    doctor = Doctor(name, phone, cpf, birth, salary, on_call=False, available=True)
                    self.__dao.add(doctor.cpf, doctor)
                    self.__view.display_msg('Médico cadastado com sucesso!', success=True)
            else:
                self.__view.display_msg('Já existe um médico com esse CPF.', success=False)
        self.__system_controller.open_doctor_view()

    def edit_doctor(self):
        cpf = self.__view.ask_for_cpf()
        if cpf:
            doc = self.find_doctor_by_cpf(cpf)
            if doc is not None:
                edited_doctor = self.__view.edit_doctor(doc)
                if edited_doctor:
                    new_cpf, name, phone, birth, salary, on_call, available = edited_doctor
                    doc.cpf = new_cpf
                    doc.name = name
                    doc.phone_number = phone
                    doc.date_of_birth = birth
                    doc.salary = salary
                    doc.on_call = on_call
                    doc.available = available
                    self.__dao.remove(cpf)
                    self.__dao.add(new_cpf, doc)
                    self.__view.display_msg('Dados do médico alterados com sucesso!', success=True)
        self.__system_controller.open_doctor_view()

    def get_doctor(self):
        cpf = self.__view.ask_for_cpf()
        if cpf:
            doc = self.find_doctor_by_cpf(cpf)
            if doc is not None:
                self.__view.display_doctor(doc)
        self.__system_controller.open_doctor_view()

    def delete_doctor(self):
        """
        Deletes doctor by cpf
        :return:
        """
        cpf = self.__view.ask_for_cpf()
        if cpf:
            doc = self.find_doctor_by_cpf(cpf)
            if doc is not None:
                if self.__view.confirm_doctor_deletion(doc):
                    self.__dao.remove(doc.cpf)
                    self.__view.display_msg('Médico excluído com sucesso!', success=True)
        self.__system_controller.open_doctor_view()

    def get_on_call_doctors(self):
        self.__view.list_on_call_doctors([doc for doc in self.__dao.get_all() if doc.on_call])
        self.__system_controller.open_doctor_view()

    def call_doctor(self):
        delay_time = randint(5, 15)
        docs = self.__dao.get_all()
        on_call = [doc for doc in docs if doc.on_call]
        rest = [doc for doc in docs if not doc.on_call]
        doc = self.__view.list_available_doctors_to_call(on_call + rest)
        if doc:
            print(f'delay sem plantao: {delay_time}')
            if doc.on_call:
                delay_time = int(delay_time / 2)
                print(f'delay com plantao: {delay_time}')
            self.__view.display_msg(f'O doutor {doc.name} foi chamado e chegará em {delay_time} minutos', success=True)
        self.__system_controller.open_doctor_view()
