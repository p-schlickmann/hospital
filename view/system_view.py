import PySimpleGUI as sg

from .base_view import BaseView


class SystemView(BaseView):
    def __init__(self):
        super().__init__(self)
        self.__window = None

    @property
    def window(self):
        return self.__window

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
