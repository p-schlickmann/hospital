from datetime import datetime


class Log:
    def __init__(self, id: int, title: str, description: str, happened_at: datetime):
        self.__id = id
        self.__title = title
        self.__description = description
        self.__happened_at = happened_at

    def __str__(self):
        return f'{self.id} | {self.title} | {self.happened_at.strftime("%d/%m/%Y %H:%M")}'
        
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id: int):
        self.__id = id
        
    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, title: str):
        self.__title = title
        
    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, description: str):
        self.__description = description
        
    @property
    def happened_at(self):
        return self.__happened_at
    
    @happened_at.setter
    def happened_at(self, happened_at: datetime):
        self.__happened_at = happened_at
