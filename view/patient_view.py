from model.health_status import POSSIBLE_STATUS
from .base_view import BaseView


class PatientView(BaseView):
    def __init__(self):
        super().__init__()

    def display_options(self):
        """
        Displays system options
        :return: chosen option
        """
        self.display_header('Pacientes')
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

    def open(self):
        pass

    def close(self):
        pass

    def show_waiting_line(self, line: list):
        """
        Display patient waiting line on the screen
        :param line: list of patients in the line
        :return: None
        """
        if not line:
            self.display_msg('[-] A fila de pacientes está vazia.')
        for i, patient in enumerate(line):
            print(f'{i + 1}. {patient["patient"].name} | gravidade: {patient["severity"]}')

    def get_health_status(self, patient):
        """
        Displays input to get new patient health status
        :param patient: Patient instance
        :return: new health status, None if chosen status is invalid
        """
        print('Selecione um estado de saúde para o paciente')
        for idx, status in enumerate(POSSIBLE_STATUS):
            print(f'[{idx + 1}] {status} {"(atual)" if status == patient.health_status else ""}')
        possible_indexes = {idx for idx, status in enumerate(POSSIBLE_STATUS)}
        chosen_status = self.read_whole_number(input('Digite o número do status desejado: '), possible_indexes)
        if chosen_status:
            return POSSIBLE_STATUS[chosen_status - 1]

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

    def display_patient_condition(self, patient, admittion_count):
        print('-----------------')
        print(f'{admittion_count} vez no hospital.')
        arrived_at = patient.arrived_at
        if arrived_at:
            print(f'Chegou: {arrived_at}')
        admitted_at = patient.admitted_at
        if admitted_at:
            print(f'Admitido em: {admitted_at}')
        doctors = patient.doctors
        if doctors:
            print(f'Médicos: ')
            for doc in doctors:
                print(f'- {doc}')
        discharged_at = patient.discharged_at
        if discharged_at:
            print(f'Alta: {discharged_at}')
        if patient.illnesses:
            print('Doenças: ')
            for illness in patient.illnesses:
                print(f'- {illness}')
        if patient.symptoms:
            print('Sintomas: ')
            for symptom in patient.symptoms:
                print(f'- {symptom}')

    def display_patient_history(self, previous_admittions):
        if not previous_admittions:
            print('[-] Esse paciente não tem histórico de internação no nosso hospital')
        else:
            self.display_person_info(previous_admittions[0], only_base_info=True)
            for idx, patient in enumerate(previous_admittions):
                self.display_patient_condition(patient, idx + 1)

    def get_doctors_that_diagnosed_the_patient(self):
        print('Digite o CPF de um dos médicos que atendeu esse paciente (deixar em branco para pular): ')
        cpfs = []
        add_another = True
        while add_another:
            cpf = input('CPF: ')
            cpfs.append(cpf)
            if not cpf:
                break
            add_another = self.confirm_action('Adicionar outro médico?')
        return cpfs