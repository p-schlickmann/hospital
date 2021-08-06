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
        print("2 - Atender paciente da fila")
        print("3 - Dar alta para paciente")
        print("4 - Ver dados/histórico de um paciente")
        print("5 - Excluir paciente")
        print("6 - Ver fila de atendimento")
        print("7 - Atualizar estado de saúde de um paciente")
        print("0 - Voltar ao menu principal")
        chosen_option = input("Digite o número da opção desejada: ")
        return self.read_whole_number(chosen_option, {0, 1, 2, 3, 4, 5, 6, 7})

    @staticmethod
    def show_waiting_line(line: list):
        """
        Display patient waiting line on the screen
        :param line: list of patients in the line
        :return: None
        """
        for i, patient in enumerate(line):
            print(f'{i + 1}. {patient}')

    def update_health_status(self, possible_status, patient):
        """
        Displays input to get new pacient health status
        :param possible_status: list of possible health status a patient can have
        :param patient: Patient instance
        :return: new health status
        """
        print('Selecione o novo estado de saúde do paciente encontrado')
        for status in possible_status:
            print(f'[1] {status} {"(atual)" if status == patient.health_status.status else ""}')
        possible_indexes = {idx for idx, status in enumerate(possible_status)}
        return self.read_whole_number(input('Digite o número do status desejado: '), possible_indexes) - 1

    @staticmethod
    def ask_for_emergency_contact():
        return input('Contato de emergência com DDD (opcional, apenas números): ')

    @staticmethod
    def use_this_registry():
        """
        Asks if the user wants to use the previously registered patient info
        :return: True if yes, False otherwise
        """
        answer = input('Deseja usar esse cadastro? [s/N]: ')
        return answer in {'s', 'S'}

    @staticmethod
    def enter_illnesses():
        """
        Enter patient identified illnesses
        :return: list of entered illnesses
        """
        illnesses = []
        while True:
            name = input('Nome da doença: ')
            description = input('Descrição: ')
            severity = input('Gravidade: ')
            illnesses.append({'name': name, 'description': description, 'severity': severity})
            add_another = input('Adicionar outra doença? [s/N]: ')
            if add_another not in {'s', 'S'}:
                break
        return illnesses

    @staticmethod
    def enter_symptoms():
        """
        Enter patient identified symptoms
        :return: list of entered symptoms
        """
        symptoms = []
        while True:
            name = input('Nome do sintoma: ')
            description = input('Descrição: ')
            discomfort_level = input('Grau de desconforto (0 a 10): ')
            symptoms.append({'name': name, 'description': description, 'discomfort_level': discomfort_level})
            add_another = input('Adicionar outro sintoma? [s/N]: ')
            if add_another not in {'s', 'S'}:
                break
        return symptoms

    def display_patient_condition(self, patient):
        print('1 vez no hospital.')
        print('Doenças: ')
        for illness in patient.ilnesses:
            print(f'- {illness}')
        print('Sintomas: ')
        for symptom in patient.symptoms:
            print(f'- {symptom}')

    def display_patient_history(self, previous_admittions):
        if not previous_admittions:
            print('[-] Esse paciente não tem histórico de internação no nosso hospital')
        else:
            self.display_person_info(previous_admittions[0])
            for patient in previous_admittions:
                self.display_patient_condition(patient)
