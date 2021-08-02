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
        print("1 - Admitir paciente")
        print("2 - Dar alta para paciente")
        print("3 - Ver dados/histórico de um paciente")
        print("4 - Excluir paciente")
        print("5 - Ver fila de atendimento")
        print("6 - Atualizar estado de saúde de um paciente")
        print("0 - Voltar ao menu principal")
        chosen_option = input("Digite o número da opção desejada: ")
        return self.read_whole_number(chosen_option, {0, 1, 2, 3, 4, 5, 6})

    @staticmethod
    def show_waiting_line(line: list):
        """
        Display patient waiting line on the screen
        :param line: list of patients in the line
        :return: None
        """
        for i, patient in enumerate(line):
            print(f'{i + 1}. {patient}')

    def update_health_status(self, patient):
        """
        Displays input to get new pacient health status
        :param patient: Patient instance
        :return: new health status
        """
        print('Estados possiveis')
        return input('Novo estado de saúde (atual: Critico): ')

    def ask_for_emergency_contact(self):
        return input('Contato de emergência com DDD (opcional, apenas números): ')

    def diagnose(self, pacient):
        pass

    def use_this_registry(self):
        """
        Asks if the user wants to use the previously registered patient info
        :return: True if yes, False otherwise
        """
        answer = input('Deseja usar esse cadastro? [s/N]: ')
        return answer in {'s', 'S'}
