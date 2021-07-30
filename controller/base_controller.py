from abc import ABC, abstractmethod


class BaseController(ABC):
    @abstractmethod
    def __init__(self, view, controller=None):
        self.__view = view
        self.__controller = controller

    def open_view(self, options: dict):
        while True:
            chosen_option = self.__view.display_options()
            if chosen_option is not None:
                options[chosen_option]()

    def return_to_main_menu(self):
        """
        Goes back to the system controller view
        :return: None
        """
        if self.__controller is not None:
            return self.__controller.open_main_view()

