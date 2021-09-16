import PySimpleGUI as sg

from .base_view import BaseView


class SystemView(BaseView):
    def __init__(self):
        super().__init__()
        self.__window = None

    def init_components(self):
        sg.ChangeLookAndFeel('Reddit')
        window = sg.Window('Hospital Mendes', element_justification='c').Layout([
            [sg.Text('Bem vindo ao Hospital Mendes, selecione uma opção:', font=('Helvetica', 25))],
            [
                self.blue_button('Pacientes', 1),
                self.blue_button('Médicos', 2)
            ],
            [
                self.blue_button('Logs', 3),
                self.blue_button('Sair', 0)
            ]
        ])
        self.__window = window

    def open(self):
        button, values = self.__window.Read()
        return button, values

    def close(self):
        try:
            self.__window.Close()
        except AttributeError:
            pass
