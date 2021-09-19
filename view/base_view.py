from abc import ABC, abstractmethod

import PySimpleGUI as sg

from model.doctor import Doctor
from model.patient import Patient


class BaseView(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @staticmethod
    def read_whole_number(chosen_number: str, valid_numbers: set = None):
        """
        Reads and processes chosen number
        :return: chosen number integer, or None if the number was invalid
        """
        try:
            chosen_number_int = int(chosen_number)
            if valid_numbers and chosen_number_int not in valid_numbers:
                raise ValueError
            return chosen_number_int
        except ValueError:
            print('Valor numérico incorreto. Digite um inteiro válido.')
            if valid_numbers:
                print(f'Inteiros válidos: {valid_numbers}')

    @staticmethod
    def format_menu_name_to_fit_hospital_header(name):
        """
        Formats passed menu name to add dashes to its side till if fits hospital header
        :param name: str
        :return: formatted menu name
        """
        name_len = len(name)
        if name_len >= 33:
            return name
        else:
            name = ' ' + name + ' '
            name_has_needed_len = len(name) >= 34
            while not name_has_needed_len:
                name = '-' + name + '-'
                name_has_needed_len = len(name) >= 34
            return name

    def display_header(self, menu_name):
        print('')
        print("-------- Hospital Mendes ---------")
        print(self.format_menu_name_to_fit_hospital_header(menu_name))

    @staticmethod
    def display_msg(msg: str, success):
        sg.Popup('Sucesso' if success else 'Erro', msg, font=('Helvetica', 15))

    @staticmethod
    def display_person_info(person, only_base_info=False):
        """
        Checks if person is a patient or a doctor, and then displays info accordingly
        :param person: patient or doctor instance
        :return: None
        """
        print(f'Nome: {person.name}')
        print(f'Data de nascimento: {person.date_of_birth}')
        print(f'CPF: {person.cpf}')
        print(f'Celular: {person.phone_number}')
        if isinstance(person, Doctor):
            print(f'Salário: {person.salary}')
            print(f'Disponível: {"sim" if person.available else "nao"}')
            print(f'De plantão: {"sim" if person.on_call else "nao"}')
        elif isinstance(person, Patient):
            if not only_base_info:
                arrived_at = person.arrived_at
                if arrived_at:
                    print(f'Chegou: {arrived_at}')
                admitted_at = person.admitted_at
                if admitted_at:
                    print(f'Admitido em: {admitted_at}')
                doctors = person.doctors
                if doctors:
                    print(f'Médicos: ')
                    for doc in doctors:
                        print(f'- {doc}')
                discharged_at = person.discharged_at
                if discharged_at:
                    print(f'Alta: {discharged_at}')
            print(f'Contato de emergência: {person.emergency_contact}')

    @staticmethod
    def confirm_action(msg):
        return input(f'[?] {msg}? [s/N]: ') in {'s', 'S'}

    @staticmethod
    def blue_button(name, key):
        return sg.Button(name, key=key, size=(15, 1.3), font=('Helvetica', 15))