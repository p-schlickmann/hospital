from .base_view import BaseView


class SystemView(BaseView):
    def __init__(self):
        super().__init__()

    def display_options(self):
        """
        Displays system options
        :return: chosen option
        """
        print("-------- Hospital Mendes ---------")
        print("1 - Pacientes")
        print("2 - Médicos")
        print("3 - Logs")
        print("0 - Finalizar sistema")
        chosen_option = input("Digite o número da opção desejada: ")
        return self.read_whole_number(chosen_option, {0, 1, 2, 3})
