class HealthStatus:
    def __init__(self, status: str):
        self.__status = status
        
    @property
    def status(self):
        return self.__status
