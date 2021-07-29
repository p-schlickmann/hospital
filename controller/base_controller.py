from abc import ABC, abstractmethod


class BaseController(ABC):
    @abstractmethod
    def __init__(self, view):
        self.__view = view

    def open_view(self, options: dict):
        while True:
            chosen_option = self.__view.display_options()
            if chosen_option is not None:
                options[chosen_option]()

