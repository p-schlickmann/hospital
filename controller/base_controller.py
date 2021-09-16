from abc import ABC, abstractmethod


class BaseController(ABC):
    @abstractmethod
    def __init__(self, view, controller=None):
        self.__view = view
        self.__controller = controller

    def open_view(self, options: dict):
        self.__view.init_components()
        chosen_option, _ = self.__view.open()
        if chosen_option is not None:
            self.__view.close()
            options[chosen_option]()

    def return_to_main_menu(self):
        """
        Goes back to the system controller view
        :return: None
        """
        self.__view.close()
        if self.__controller is not None:
            return self.__controller.open_main_view()

