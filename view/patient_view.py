import PySimpleGUI as sg

from model.health_status import POSSIBLE_STATUS
from .base_view import BaseView


class PatientView(BaseView):
    def __init__(self):
        super().__init__()
        self.__window = None

    def init_components(self):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Pacientes', element_justification='c').Layout([
            [sg.Text('Pacientes', font=('Helvetica', 25))],
            [
                self.blue_button('Admitir', 1),
                self.blue_button('Atender', 2)
            ],
            [
                self.blue_button('Dar alta', 3),
                self.blue_button('Ver dados/histórico', 4)
            ],
            [
                self.blue_button('Ver fila de atendimento', 6),
                self.blue_button('Atualizar estado de saúde', 7),
            ],
            [
                self.blue_button('Excluir', 5),
                self.blue_button('Menu principal', 0)
            ]
        ])
        self.__window = window

    def open(self):
        button, values = self.__window.Read()
        return button, values

    def close(self):
        self.__window.Close()

    def show_waiting_line(self, line: list):
        """
        Display patient waiting line on the screen
        :param line: list of patients in the line
        :return: None
        """
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Pacientes - Listar', element_justification='c').Layout([
            [sg.Text('Fila de atendimento', font=('Helvetica', 25))],
            [[sg.Text('A fila de pacientes está vazia. :)', font=('Helvetica', 20))] for _ in range(1) if not line],
            [
                [
                    sg.Text(f'{idx + 1}. {patient["patient"].name} | gravidade: {patient["severity"]}',
                            font=('Helvetica', 20))] for idx, patient in enumerate(line)
            ],
            [self.blue_button('Voltar', 0)]
        ])
        self.__window = window
        self.open()
        self.close()

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

    def ask_for_cpf(self):
        """
        Asks for CPF
        :return: given cpf
        """

        sg.ChangeLookAndFeel('Reddit')
        input_font = ('Helvetica', 15)
        input_size = (10, 2)
        window = sg.Window('Hospital Mendes - Pacientes', element_justification='c').Layout([
            [sg.Text(f'Digite o CPF do paciente', font=('Helvetica', 25))],
            [sg.Text('CPF (apenas números)', font=input_font, size=input_size), sg.InputText(key='cpf', font=input_font)],
            [self.blue_button('Voltar', 0), self.blue_button('Ok', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        return values['cpf']

    def ask_for_main_info(self):
        """
        Display main info inputs
        :return: tuple containing info gathered from the inputs
        """
        input_font = ('Helvetica', 15)
        input_size = (20, 2)
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Pacientes - Admitir', element_justification='c').Layout([
            [sg.Text('Admitir paciente', font=('Helvetica', 25))],
            [sg.Text('Nome completo', font=input_font, size=input_size), sg.InputText(key='name', font=input_font)],
            [sg.Text('Telefone com DDD', font=input_font, size=input_size), sg.InputText(key='phone', font=input_font)],
            [sg.Text('Contato de emergência com DDD', font=input_font, size=input_size),
             sg.InputText(key='emergency', font=input_font)],
            [sg.Text('Data de nascimento (DD/MM/AAAA)', font=input_font, size=input_size), sg.InputText(key='date_of_birth', font=input_font)],

            [self.blue_button('Cancelar', 0), self.blue_button('Admitir', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        return values['name'], values['phone'], values['emergency'], values['date_of_birth']


    @staticmethod
    def ask_for_emergency_contact():
        return input()

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