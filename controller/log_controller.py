from datetime import datetime

from controller.base_controller import BaseController
from data.data_access_object import DataAccessObject
from model.log import Log
from view.log_view import LogView


class LogController(BaseController):
    def __init__(self, system_controller):
        self.__system_controller = system_controller
        self.__view = LogView()
        self.__dao = DataAccessObject('data/logs.pkl', Log)
        super().__init__(self.__view, self.__system_controller)

    def new_log(self):
        log_info = self.__view.new_log()
        if log_info:
            id, title, desc = log_info
            if not id or not title:
                self.__view.display_msg('Especifique pelo menos um titulo e um id!', success=False)
            else:
                log = Log(id, title, desc, datetime.now())
                self.__dao.add(log.id, log)
                self.__view.display_msg('Log criado com sucesso!', success=True)
        self.__system_controller.open_log_view()

    def find_log_by_id(self, id):
        log = self.__dao.get(id)
        if log:
            return log
        else:
            self.__view.display_msg(f'Nenhum log encontrado com esse id! ({id})', success=False)

    def edit_log(self):
        id = self.__view.ask_for_log_id()
        if id:
            log = self.find_log_by_id(id)
            if log is not None:
                edit_log_info = self.__view.edit_log(log)
                if edit_log_info:
                    title, desc = edit_log_info
                    if title:
                        log.title = title
                    if desc:
                        log.description = desc
                    self.__dao.add(log.id, log)
                    self.__view.display_msg('Log editado com sucesso!', success=True)
        self.__system_controller.open_log_view()

    def delete_log(self):
        """
        Deletes log by id
        :return:
        """
        id = self.__view.ask_for_log_id()
        if id:
            log_to_remove = self.find_log_by_id(id)
            if log_to_remove is not None:
                confirmed = self.__view.confirm_log_deletion(log_to_remove)
                if confirmed:
                    self.__dao.remove(log_to_remove.id)
                    self.__view.display_msg('Log excluído com sucesso!', success=True)
        self.__system_controller.open_log_view()

    def list_logs(self):
        logs = self.__dao.get_all()
        self.__view.list_logs(logs)
        self.__system_controller.open_log_view()
