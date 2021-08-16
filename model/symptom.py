class Symptom:
    def __init__(self, name: str, description: str, discomfort_level: int):
        self.__name = name
        self.__description = description
        self.__discomfort_level = discomfort_level

    def __str__(self):
        return f'{self.name} | {self.description} | Desconforto: {self.discomfort_level}'
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name
        
    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, description: str):
        self.__description = description
        
    @property
    def discomfort_level(self):
        return self.__discomfort_level
    
    @discomfort_level.setter
    def discomfort_level(self, discomfort_level: int):
        self.__discomfort_level = discomfort_level
        
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id: int):
        self.__id = id
