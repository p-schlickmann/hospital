import PySimpleGUI as sg

from model.health_status import POSSIBLE_STATUS
from .base_view import BaseView


class PatientView(BaseView):
    def __init__(self):
        super().__init__(self)
        self.__window = None

    @property
    def window(self):
        return self.__window

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
        sg.ChangeLookAndFeel('Reddit')
        input_font = ('Helvetica', 15)
        input_size = (10, 2)
        window = sg.Window('Hospital Mendes - Pacientes - Admitir', element_justification='c').Layout([
            [sg.Text(f'Selecione um estado de saúde para o paciente', font=('Helvetica', 25))],
            [
                [sg.Text(f'[{idx + 1}] {status} {"(atual)" if status == patient.health_status else ""}', font=input_font)] for idx, status in enumerate(POSSIBLE_STATUS)
            ],
            [sg.Text('Número do status', font=input_font, size=input_size),
             sg.InputText(key='status', font=input_font)],
            [self.blue_button('Voltar', 0), self.blue_button('Salvar', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        try:
            return POSSIBLE_STATUS[int(values['status']) - 1]
        except ValueError:
            self.display_msg('Entre um numero inteiro valido!', success=False)

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

    def use_this_registry(self, patient):
        """
        Asks if the user wants to use the previously registered patient info
        :return: True if yes, False otherwise
        """
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Pacientes - Admitir', element_justification='c').Layout([
            [sg.Text('Encontramos um cadastro previamente\npreenchido para esse paciente:', font=('Helvetica', 25))],
            [sg.Text(self.display_person_info(patient), font=('Helvetica', 20))],
            [sg.Text('Deseja usar esse cadastro?', font=('Helvetica', 25))],
            [self.blue_button('Não', 0), self.blue_button('Sim', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        return int(button) == 1

    def enter_illness(self, patient):
        """
        Enter patient identified illnesses
        :return: list of entered illnesses
        """
        input_font = ('Helvetica', 15)
        input_size = (20, 2)
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Pacientes - Atender', element_justification='c').Layout([
            [sg.Text(f'Atendendo o paciente {patient.name}', font=('Helvetica', 25))],
            [sg.Text('Nome da doença', font=input_font, size=input_size), sg.InputText(key='name', font=input_font)],
            [sg.Text('Gravidade', font=input_font, size=input_size), sg.InputText(key='severity', font=input_font)],
            [sg.Text('Descrição', font=input_font, size=input_size), sg.InputText(key='desc', font=input_font)],
            [self.blue_button('Cancelar', 0), self.blue_button('Adicionar doença', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        return values['name'], values['desc'], values['severity']

    def enter_symptom(self, patient):
        """
        Enter patient identified symptoms
        :return: list of entered symptoms
        """
        input_font = ('Helvetica', 15)
        input_size = (20, 2)
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Pacientes - Atender', element_justification='c').Layout([
            [sg.Text(f'Atendendo o paciente {patient.name}', font=('Helvetica', 25))],
            [sg.Text('Nome da sintoma', font=input_font, size=input_size), sg.InputText(key='name', font=input_font)],
            [sg.Text('Grau de desconforto', font=input_font, size=input_size), sg.InputText(key='disc', font=input_font)],
            [sg.Text('Descrição', font=input_font, size=input_size), sg.InputText(key='desc', font=input_font)],
            [self.blue_button('Cancelar', 0), self.blue_button('Adicionar sintoma', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        return values['name'], values['desc'], values['disc']

    @staticmethod
    def display_patient_condition(patient, admittion_count):
        condition = [
            '_______________________________________________________________',
            f'{admittion_count} vez no hospital.',
        ]
        arrived_at = patient.arrived_at
        if arrived_at:
            condition.append(f'Chegou: {arrived_at.strftime("%d/%m/%Y %H:%M")}')
        admitted_at = patient.admitted_at
        if admitted_at:
            condition.append(f'Admitido em: {admitted_at.strftime("%d/%m/%Y %H:%M")}')
        diagnosed_at = patient.diagnosed_at
        if diagnosed_at:
            condition.append(f'Atendido em: {diagnosed_at.strftime("%d/%m/%Y %H:%M")}')
        doctors = patient.doctors
        if doctors:
            condition.append(f'Médicos: ')
            for doc in doctors:
                condition.append(f'- {doc}')
        discharged_at = patient.discharged_at
        if discharged_at:
            condition.append(f'Alta: {discharged_at.strftime("%d/%m/%Y %H:%M")}')
        if patient.illnesses:
            condition.append('Doenças: ')
            for illness in patient.illnesses:
                condition.append(f'- {illness}')
        if patient.symptoms:
            condition.append('Sintomas: ')
            for symptom in patient.symptoms:
                condition.append(f'- {symptom}')
        return '\n'.join(condition)

    def display_patient_history(self, previous_admittions):
        *_, latest_admittion = previous_admittions
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Pacientes - Ver dados/histórico', element_justification='c').Layout([
            [sg.Text('Ver dados/histórico', font=('Helvetica', 25))],
            [sg.Text(self.display_person_info(latest_admittion), font=('Helvetica', 20))],
            [[sg.Text(self.display_patient_condition(patient, idx + 1), font=('Helvetica', 20))] for idx, patient in enumerate(previous_admittions)],
            [self.blue_button('Voltar', 0)]
        ])
        self.__window = window
        self.open()
        self.close()

    def get_doctors_that_diagnosed_the_patient(self):
        cpfs = []
        i = 0
        while True:
            sg.ChangeLookAndFeel('Reddit')
            input_font = ('Helvetica', 15)
            input_size = (10, 2)
            window = sg.Window('Hospital Mendes - Pacientes', element_justification='c').Layout([
                [sg.Text(f'Digite o(s) CPF(s) do(s) médico(s) que \natendeu/atenderam esse paciente', font=('Helvetica', 25))],
                [sg.Text('CPF (apenas números)', font=input_font, size=input_size),
                 sg.InputText(key='cpf', font=input_font)],
                [self.blue_button('Finalizar', 0), self.blue_button('Adicionar' if i == 0 else 'Adicionar outro', 1)]
            ])
            self.__window = window
            button, values = self.open()
            self.close()
            i = i + 1
            if int(button) == 0:
                return cpfs
            cpfs.append(values['cpf'])

    def confirm_patient_discharge(self, patient):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Pacientes - Alta', element_justification='c').Layout([
               [sg.Text('Dar alta para o paciente encontrado?', font=('Helvetica', 25))],
               [sg.Text(patient, font=('Helvetica', 20))],
               [self.blue_button('Cancelar', 0), self.blue_button('Confirmar', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        return int(button) == 1

    def confirm_patient_deletion(self, patient):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Pacientes - Excluir', element_justification='c').Layout([
            [sg.Text('Excluir todas as informações do paciente selecionado?', font=('Helvetica', 25))],
            [sg.Text(patient, font=('Helvetica', 20))],
            [self.blue_button('Cancelar', 0), self.blue_button('Confirmar', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        return int(button) == 1
