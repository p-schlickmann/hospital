from abc import ABC, abstractmethod


class BaseView(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def display_options(self):
        pass

    @staticmethod
    def read_whole_number(chosen_number: str, valid_numbers: set = None):
        """
        Reads and processes chosen number
        :return: chosen number integer, or None if the number was invalid
        """
        try:
            chosen_number_int = int(chosen_number)
            if chosen_number_int not in valid_numbers:
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

    def ask_for_cpf(self, current_menu_name: str):
        """
        Asks for CPF
        :return: given cpf
        """
        print("-------- Hospital Mendes ---------")
        print(self.format_menu_name_to_fit_hospital_header(current_menu_name))
        return input('CPF (apenas números): ')

    @staticmethod
    def ask_for_main_info():
        """
        Display main info inputs
        :return: tuple containing info gathered from the inputs
        """
        name = input('Nome completo: ')
        phone_number = input('Telefone com DDD (apenas números): ')
        date_of_birth = input('Data de nascimento (DD/MM/AAAA): ')
        return name, phone_number, date_of_birth

    @staticmethod
    def display_msg(msg: str):
        print(msg)

    @staticmethod
    def display_person_info(person):
        """
        Checks if person is a patient or a doctor, and then displays info accordingly
        :param person:
        :return:
        """
        print('person info')

