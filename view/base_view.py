from abc import ABC, abstractmethod

import PySimpleGUI as sg

from model.doctor import Doctor


class BaseView(ABC):
    @abstractmethod
    def __init__(self, view):
        self.__view = view

    @property
    @abstractmethod
    def window(self):
        pass

    @abstractmethod
    def init_components(self):
        pass

    def open(self):
        button, values = self.__view.window.Read()
        return button, values

    def close(self):
        self.__view.window.Close()

    @staticmethod
    def display_msg(msg: str, success):
        sg.Popup('Sucesso' if success else 'Erro', msg, font=('Helvetica', 15))

    @staticmethod
    def display_person_info(person):
        """
        Checks if person is a patient or a doctor, and then displays info accordingly
        :param person: patient or doctor instance
        :return: None
        """
        info = []
        info.append(f'Nome: {person.name}')
        info.append(f'Data de nascimento: {person.date_of_birth}')
        info.append(f'CPF: {person.cpf}')
        info.append(f'Celular: {person.phone_number}')
        if isinstance(person, Doctor):
            info.append(f'Salário: {person.salary}')
            info.append(f'Disponível: {"Sim" if person.available else "Não"}')
            info.append(f'De plantão: {"Sim" if person.on_call else "Não"}')
        return '\n'.join(info)

    @staticmethod
    def blue_button(name, key):
        return sg.Button(name, key=key, size=(15, 1.3), font=('Helvetica', 15))