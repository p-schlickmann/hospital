from .base_view import BaseView


class LogView(BaseView):
    def __init__(self):
        super().__init__()

    def display_options(self):
        """
        Displays system options
        :return: chosen option
        """
        self.display_header('Logs')
        print("1 - Novo log")
        print("2 - Editar log")
        print("3 - Excluir log")
        print("4 - Listar logs")
        print("0 - Voltar ao menu principal")
        chosen_option = input("Digite o número da opção desejada: ")
        return self.read_whole_number(chosen_option, {0, 1, 2, 3, 4})

    def new_log(self):
        """
        Displays new logs required inputs
        :return: tuple with the information gathered from the inputs
        """
        id = input('Id: ')
        title = input('Título: ')
        desc = input('Descrição: ')
        return id, title, desc

    def ask_for_log_id(self):
        return input('Id do log: ')

    def edit_log(self, log):
        """
        Displays edit logs required inputs
        :return: tuple with the information gathered from the inputs
        """
        print('[+] Pressione `Enter` para pular.')
        title = input(f'Título [{log.title}]: ')
        desc = input(f'Descrição [{log.description}]: ')
        return title, desc

    def list_logs(self, logs: list):
        """
        Lists all logs of the hospital
        :return: None
        """
        for log in logs:
            print(log)
