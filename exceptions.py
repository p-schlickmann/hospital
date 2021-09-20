class NoPatientInLineException(IndexError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LogNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
