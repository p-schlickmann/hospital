class Illness:
    def __init__(self, name: str, description: str, severity: int):
        self.__name = name
        self.__description = description
        self.__severity = severity

    def __str__(self):
        return f'{self.name} | {self.description} | Gravidade: {self.severity}'
        
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
    def severity(self):
        return self.__severity
    
    @severity.setter
    def severity(self, severity: int):
        self.__severity = severity
