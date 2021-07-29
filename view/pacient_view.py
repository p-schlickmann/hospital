from .base_view import BaseView


class PatientView(BaseView):
    def __init__(self):
        super().__init__()

    def display_options(self):
        """
        Displays system options
        :return: chosen option
        """
        print("-------- Hospital Mendes ---------")
        print("------------ Pacientes -------------")
        print("1 - Cadastrar paciente")
        print("2 - Alterar paciente")
        print("3 - Buscar paciente")
        print("4 - Excluir paciente")
        print("5 - Ver fila de atendimento")
        print("0 - Voltar ao menu principal")
        chosen_option = input("Digite o número da opção desejada: ")
        return self.read_whole_number(chosen_option, {0, 1, 2, 3, 4, 5})

    @staticmethod
    def show_waiting_line(line: list):
        """
        Display patient waiting line on the screen
        :param line: list of patients in the line
        :return: None
        """
        for i, patient in enumerate(line):
            print(f'{i + 1}. {patient}')

    @staticmethod
    def show_msg(msg: str):
        print(msg)
