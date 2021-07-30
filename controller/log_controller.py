from controller.base_controller import BaseController
from view.log_view import LogView


class LogController(BaseController):
    def __init__(self, system_controller):
        self.__logs = []
        self.__system_controller = system_controller
        self.__view = LogView()
        super().__init__(self.__view, self.__system_controller)

    def new_log(self):
        pass

    def edit_log(self):
        pass

    def delete_log(self):
        """
        Deletes patient by cpf
        :return:
        """
        pass

    def list_logs(self):
        pass
