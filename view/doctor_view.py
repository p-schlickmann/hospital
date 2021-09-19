import PySimpleGUI as sg

from .base_view import BaseView


class DoctorView(BaseView):
    def __init__(self):
        super().__init__()
        self.__window = None

    def init_components(self):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Médicos', element_justification='c').Layout([
            [sg.Text('Médicos', font=('Helvetica', 25))],
            [
                self.blue_button('Listar', 4),
                self.blue_button('Criar', 1)
            ],
            [
                self.blue_button('Editar', 2),
                self.blue_button('Deletar', 3)
            ],
            [self.blue_button('Menu principal', 0)]
        ])
        self.__window = window

    def open(self):
        button, values = self.__window.Read()
        return button, values

    def close(self):
        self.__window.Close()

    def new_doctor(self):
        input_font = ('Helvetica', 15)
        input_size = (10, 2)
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Médicos - Criar', element_justification='c').Layout([
            [sg.Text('Criar médico', font=('Helvetica', 25))],
            [sg.Text('Id', font=input_font, size=input_size), sg.InputText(key='id', font=input_font)],
            [sg.Text('Título', font=input_font, size=input_size), sg.InputText(key='title', font=input_font)],
            [sg.Text('Descrição', font=input_font, size=input_size), sg.InputText(key='desc', font=input_font)],
            [self.blue_button('Cancelar', 0), self.blue_button('Criar', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        return values['id'], values['title'], values['desc']

    def ask_for_doctor_id(self):
        sg.ChangeLookAndFeel('Reddit')
        input_font = ('Helvetica', 15)
        input_size = (10, 2)
        window = sg.Window('Hospital Mendes - Médicos', element_justification='c').Layout([
            [sg.Text('Digite o id do médico', font=('Helvetica', 25))],
            [sg.Text('Id', font=input_font, size=input_size), sg.InputText(key='id', font=input_font)],
            [self.blue_button('Voltar', 0), self.blue_button('Ok', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        return values['id']

    def edit_doctor(self, doctor):
        input_font = ('Helvetica', 15)
        input_size = (10, 2)
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Médicos - Editar', element_justification='c').Layout([
            [sg.Text(f'Editar médico do id {doctor.id}', font=('Helvetica', 25))],
            [
                sg.Text('Título', font=input_font, size=input_size),
                sg.InputText(key='title', font=input_font, default_text=doctor.title)
            ],
            [
                sg.Text('Descrição', font=input_font, size=input_size),
                sg.InputText(key='desc', font=input_font, default_text=doctor.description)
            ],
            [self.blue_button('Cancelar', 0), self.blue_button('Confirmar', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        return values['title'], values['desc']

    def list_doctors(self, doctors: list):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Médicos - Listar', element_justification='c').Layout([
            [sg.Text('Listar médicos', font=('Helvetica', 25))],
            [[sg.Text(doctor, font=('Helvetica', 20))] for doctors in doctors],
            [self.blue_button('Voltar', 0)]
        ])
        self.__window = window
        self.open()
        self.close()

    def confirm_doctor_deletion(self, doctor):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Médico - Excluir', element_justification='c').Layout([
            [sg.Text('Excluir médico encontrado?', font=('Helvetica', 25))],
            [sg.Text(médico, font=('Helvetica', 20))],
            [self.blue_button('Voltar', 0), self.blue_button('Confirmar', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        return int(button) == 1

