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
    def ask_for_cpf(current_menu_name: str):
        """
        Asks for CPF
        :return: given cpf
        """
        print("-------- Hospital Mendes ---------")
        print(current_menu_name)
        return input('CPF (apenas números): ')

    @staticmethod
    def ask_for_main_info():
        """
        Display main info inputs
        :return: dict containing info gathered from the inputs
        """
        info = {}
        info['name'] = input('Nome completo: ')
        info['phone_number'] = input('Telefone com DDD (apenas números): ')
        info['date_of_birth'] = input('Data de nascimento (DD/MM/AAAA): ')
        return info

    @staticmethod
    def display_msg(msg: str):
        print(msg)
