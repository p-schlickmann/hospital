import PySimpleGUI as sg

from .base_view import BaseView


class LogView(BaseView):
    def __init__(self):
        super().__init__()
        self.__window = None

    def init_components(self):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Logs', element_justification='c').Layout([
            [sg.Text('Logs', font=('Helvetica', 25))],
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

    def new_log(self):
        """
        Displays new logs required inputs
        :return: tuple with the information gathered from the inputs
        """
        input_font = ('Helvetica', 15)
        input_size = (10, 2)
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Logs - Criar', element_justification='c').Layout([
            [sg.Text('Criar log', font=('Helvetica', 25))],
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

    def ask_for_log_id(self):
        sg.ChangeLookAndFeel('Reddit')
        input_font = ('Helvetica', 15)
        input_size = (10, 2)
        window = sg.Window('Hospital Mendes - Logs', element_justification='c').Layout([
            [sg.Text('Digite o id do log', font=('Helvetica', 25))],
            [sg.Text('Id', font=input_font, size=input_size), sg.InputText(key='id', font=input_font)],
            [self.blue_button('Voltar', 0), self.blue_button('Ok', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        return values['id']

    def edit_log(self, log):
        """
        Displays edit logs required inputs
        :return: tuple with the information gathered from the inputs
        """
        input_font = ('Helvetica', 15)
        input_size = (10, 2)
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Logs - Editar', element_justification='c').Layout([
            [sg.Text(f'Editar log de id {log.id}', font=('Helvetica', 25))],
            [
                sg.Text('Título', font=input_font, size=input_size),
                sg.InputText(key='title', font=input_font, default_text=log.title)
            ],
            [
                sg.Text('Descrição', font=input_font, size=input_size),
                sg.InputText(key='desc', font=input_font, default_text=log.description)
            ],
            [self.blue_button('Cancelar', 0), self.blue_button('Confirmar', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        if int(button) == 0:
            return False
        return values['title'], values['desc']

    def list_logs(self, logs: list):
        """
        Lists all logs of the hospital
        :return: None
        """
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Logs - Listar', element_justification='c').Layout([
            [sg.Text('Listar logs', font=('Helvetica', 25))],
            [[sg.Text('O hospital ainda não tem logs :(', font=('Helvetica', 20))] for _ in range(1) if not logs],
            [[sg.Text(log, font=('Helvetica', 20))] for log in logs],
            [self.blue_button('Voltar', 0)]
        ])
        self.__window = window
        self.open()
        self.close()

    def confirm_log_deletion(self, log):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes - Logs - Excluir', element_justification='c').Layout([
            [sg.Text('Excluir log encontrado?', font=('Helvetica', 25))],
            [sg.Text(log, font=('Helvetica', 20))],
            [self.blue_button('Voltar', 0), self.blue_button('Confirmar', 1)]
        ])
        self.__window = window
        button, values = self.open()
        self.close()
        return int(button) == 1
