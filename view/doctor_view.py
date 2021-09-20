import PySimpleGUI as sg

from .base_view import BaseView


class DoctorView(BaseView):
    def __init__(self):
        super().__init__(self)
        self.__window = None

    @property
    def window(self):
        return self.__window

    def init_components(self):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Médicos', element_justification='c').Layout([
            [sg.Text('Médicos', font=('Helvetica', 25))],
            [
                self.blue_button('Cadastrar', 1),
                self.blue_button('Alterar', 2)
            ],
            [
                self.blue_button('Buscar', 3),
                self.blue_button('Excluir', 4)
            ],
            [
                self.blue_button('De plantão', 5),
                self.blue_button('Chamar médico', 6)
            ],
            [self.blue_button('Menu principal', 0)]
        ])
        self.__window = window

    def ask_for_cpf(self):
        """
        Asks for CPF
        :return: given cpf
        """

        sg.ChangeLookAndFeel('Reddit')
        input_font = ('Helvetica', 15)
        input_size = (10, 2)
        window = sg.Window('Hospital Mendes - Médicos', element_justification='c').Layout([
            [sg.Text(f'Digite o CPF do médico', font=('Helvetica', 25))],
            [sg.Text('CPF (apenas números)', font=input_font, size=input_size), sg.InputText(key='cpf', font=input_font)],
            [self.blue_button('Voltar', 0), self.blue_button('Ok', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        return values['cpf']

    def new_doctor(self):
        input_font = ('Helvetica', 15)
        input_size = (20, 2)
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Médicos - Cadastrar', element_justification='c').Layout([
            [sg.Text('Cadastrar médico', font=('Helvetica', 25))],
            [sg.Text('Nome completo', font=input_font, size=input_size), sg.InputText(key='name', font=input_font)],
            [sg.Text('Telefone com DDD', font=input_font, size=input_size), sg.InputText(key='phone', font=input_font)],
            [sg.Text('Data de nascimento (DD/MM/AAAA)', font=input_font, size=input_size),
             sg.InputText(key='date_of_birth', font=input_font)],
            [sg.Text('Salário(anual)', font=input_font, size=input_size), sg.InputText(key='salary', font=input_font)],

            [self.blue_button('Cancelar', 0), self.blue_button('Criar', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        return values['name'], values['phone'], values['date_of_birth'], values['salary']

    def edit_doctor(self, doctor):
        input_font = ('Helvetica', 15)
        input_size = (20, 2)
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Médicos - Editar', element_justification='c').Layout([
            [sg.Text(f'Editando o médico {doctor}', font=('Helvetica', 25))],
            [
                sg.Text('CPF (apenas numeros)', font=input_font, size=input_size),
                sg.InputText(key='cpf', font=input_font, default_text=doctor.cpf)
            ],
            [
                sg.Text('Nome completo', font=input_font, size=input_size),
                sg.InputText(key='name', font=input_font, default_text=doctor.name)
            ],
            [
                sg.Text('Telefone com DDD', font=input_font, size=input_size),
                sg.InputText(key='phone', font=input_font, default_text=doctor.phone_number)
            ],
            [
                sg.Text('Data de nascimento (DD/MM/AAAA)', font=input_font, size=input_size),
                sg.InputText(key='birth', font=input_font, default_text=doctor.date_of_birth)
            ],
            [
                sg.Text('Salário (anual)', font=input_font, size=input_size),
                sg.InputText(key='salary', font=input_font, default_text=doctor.salary)
            ],
            [
                sg.Checkbox('De plantão', key='on_call', font=input_font, default=doctor.on_call)
            ],
            [
                sg.Checkbox('Disponível', key='available', font=input_font, default=doctor.available)
            ],
            [self.blue_button('Cancelar', 0), self.blue_button('Confirmar', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        return (
            values['cpf'], values['name'], values['phone'], values['birth'],
            values['salary'], values['on_call'], values['available']
        )

    def display_doctor(self, doctor):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Médicos - Buscar', element_justification='c').Layout([
            [sg.Text(self.display_person_info(doctor), font=('Helvetica', 20))],
            [self.blue_button('Voltar', 0)]
        ])
        self.__window = window
        self.open()
        self.close()

    def confirm_doctor_deletion(self, doctor):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Médicos - Excluir', element_justification='c').Layout([
            [sg.Text('Excluir médico selecionado?', font=('Helvetica', 25))],
            [sg.Text(doctor, font=('Helvetica', 20))],
            [self.blue_button('Cancelar', 0), self.blue_button('Confirmar', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        return int(button) == 1

    def list_on_call_doctors(self, doctors: list):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Médicos - De plantão', element_justification='c').Layout([
            [sg.Text('Listar médicos de plantão', font=('Helvetica', 25))],
            [[sg.Text('Nenhum médico de plantão :O', font=('Helvetica', 20))] for _ in range(1) if not doctors],
            [[sg.Text(doctor, font=('Helvetica', 20))] for doctor in doctors],
            [self.blue_button('Voltar', 0)]
        ])
        self.__window = window
        self.open()
        self.close()

    def list_available_doctors_to_call(self, docs):
        sg.ChangeLookAndFeel('Reddit')
        input_font = ('Helvetica', 15)
        input_size = (10, 2)
        if not docs:
            window = sg.Window('Hospital Mendes - Médicos - Chamar', element_justification='c').Layout([
                [sg.Text('Escolha um médico para chamar', font=('Helvetica', 25))],
                [sg.Text('Nenhum médico disponível :O', font=('Helvetica', 20))],
                [self.blue_button('Voltar', 0)]
            ])
        else:
            window = sg.Window('Hospital Mendes - Médicos - Chamar', element_justification='c').Layout([
                [sg.Text('Escolha um médico para chamar', font=('Helvetica', 25))],
                [[sg.Text(f'[{idx + 1}] {doctor.name}{" | PLANTÃO" if doctor.on_call else ""}', font=('Helvetica', 20))] for
                 idx, doctor in enumerate(docs)],
                [sg.Text('Número', font=input_font, size=input_size), sg.InputText(key='idx', font=input_font)],
                [self.blue_button('Voltar', 0), self.blue_button('Confirmar', 1)]
            ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        try:
            return docs[int(values['idx']) - 1]
        except ValueError:
            self.display_msg('Entre um numero inteiro válido', success=False)
