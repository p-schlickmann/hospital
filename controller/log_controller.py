from datetime import datetime

from controller.base_controller import BaseController
from model.log import Log
from view.log_view import LogView


class LogController(BaseController):
    def __init__(self, system_controller):
        self.__logs = []
        self.__system_controller = system_controller
        self.__view = LogView()
        super().__init__(self.__view, self.__system_controller)

    def new_log(self):
        self.__view.display_header('Novo log')
        id, title, desc = self.__view.new_log()
        log = Log(id, title, desc, datetime.now())
        self.__logs.append(log)
        self.__view.display_msg('[+] Log criado com sucesso!')

    def find_log_by_id(self, id):
        logs_found = [log for log in self.__logs if log.id == id]
        if logs_found:
            return logs_found[0]
        else:
            self.__view.display_msg(f'[-] Nenhum log encontrado com esse id! ({id})')

    def edit_log(self):
        self.__view.display_header('Editar log')
        id = self.__view.ask_for_log_id()
        log = self.find_log_by_id(id)
        if log is not None:
            title, desc = self.__view.edit_log(log)
            if title:
                log.title = title
            if desc:
                log.description = desc
            self.__view.display_msg('[+] Log editado com sucesso!')

    def delete_log(self):
        """
        Deletes log by id
        :return:
        """
        self.__view.display_header('Excluir log')
        id = self.__view.ask_for_log_id()
        log_to_remove = self.find_log_by_id(id)
        if log_to_remove is not None:
            self.__logs = [log for log in self.__logs if log.id != log_to_remove.id]
            self.__view.display_msg('[+] Log excluído com sucesso!')

    def list_logs(self):
        self.__view.display_header('Listar logs')
        if not self.__logs:
            self.__view.display_msg('[-] O hospital ainda não tem logs.')
        self.__view.list_logs(self.__logs)
