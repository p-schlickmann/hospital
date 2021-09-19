from random import randint

from controller.base_controller import BaseController
from model.doctor import Doctor
from view.doctor_view import DoctorView


class DoctorController(BaseController):
    def __init__(self, system_controller):
        self.__doctors = []
        self.__system_controller = system_controller
        self.__view = DoctorView()
        super().__init__(self.__view, self.__system_controller)

    def find_doctor_by_cpf(self, cpf, display_not_found_msg=True):
        """
        Searches for doctor with the given cpf
        :return: Doctor if found, otherwise None
        """
        doctors_found = [doc for doc in self.__doctors if doc.cpf == cpf]
        if not doctors_found:
            if display_not_found_msg:
                self.__view.display_msg(f'[-] Nenhum médico foi encontrado com esse CPF ({cpf}).')
                self.__view.display_msg('[!] Verifique se o cpf é valido e foi digitado apenas com números.')
        else:
            return doctors_found[0]

    def register_doctor(self):
        self.__view.display_header('Cadastrar médico')
        cpf = self.__view.ask_for_cpf()
        if not self.find_doctor_by_cpf(cpf, display_not_found_msg=False):
            name, phone, birth, salary = self.__view.display_register_doctor()
            doctor = Doctor(name, phone, cpf, birth, salary, on_call=False, available=True)
            self.__doctors.append(doctor)
            self.__view.display_msg('[+] Médico cadastado com sucesso!')
        else:
            self.__view.display_msg('[!] Já existe um médico com esse CPF.')

    def edit_doctor(self):
        self.__view.display_header('Alterar médico')
        cpf = self.__view.ask_for_cpf()
        doc = self.find_doctor_by_cpf(cpf)
        if doc is not None:
            cpf, name, phone, birth, salary, available, on_call = self.__view.display_edit_doctor(doc)
            if cpf:
                doc.cpf = cpf
            if name:
                doc.name = name
            if phone:
                doc.phone_number = phone
            if birth:
                doc.date_of_birth = birth
            if salary:
                doc.salary = salary
            if available:
                doc.available = True if available in {'sim', 's', 'S', 'Sim'} else False
            if on_call:
                doc.on_call = True if on_call in {'sim', 's', 'S', 'Sim'} else False
            self.__view.display_msg('[+] Dados do médico alterados com sucesso!')

    def get_doctor(self):
        self.__view.display_header('Buscar médico')
        cpf = self.__view.ask_for_cpf()
        doc = self.find_doctor_by_cpf(cpf)
        if doc is not None:
            self.__view.display_msg('[+] Um médico encontrado')
            self.__view.display_person_info(doc)

    def delete_doctor(self):
        """
        Deletes doctor by cpf
        :return:
        """
        self.__view.display_header("Excluir médico")
        cpf = self.__view.ask_for_cpf()
        doc = self.find_doctor_by_cpf(cpf)
        if doc is not None:
            self.__view.display_person_info(doc)
            confirmed = self.__view.confirm_action('Excluir médico selecionado?')
            if confirmed:
                self.__doctors = [doc for doc in self.__doctors if doc.cpf == cpf]
                self.__view.display_msg('[+] Médico excluído com sucesso!')

    def get_on_call_doctors(self):
        self.__view.display_header('Listar médicos de plantão')
        self.__view.list_on_call_doctors([doc for doc in self.__doctors if doc.on_call])

    def call_doctor(self):
        self.__view.display_header('Chamar médico')
        delay_time = randint(5, 15)
        on_call = [doc for doc in self.__doctors if doc.on_call]
        rest = [doc for doc in self.__doctors if not doc.on_call]
        doc = self.__view.list_available_doctors_to_call(on_call, rest)
        if doc:
            print(f'delay sem plantao: {delay_time}')
            if doc.on_call:
                delay_time = int(delay_time / 2)
                print(f'delay com plantao: {delay_time}')

            self.__view.display_msg(f'[+] O doutor {doc.name} foi chamado e chegará em {delay_time} minutos')
