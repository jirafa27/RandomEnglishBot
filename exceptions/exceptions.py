class NotEnglishTextException(Exception):
    """
    Исключение, которое выбрасывается, если переданный текст не является английским.
    """

    def __init__(self, message="Переданный текст не является английским."):
        self.message = message
        super().__init__(self.message)


class NotRussianTextException(Exception):
    """
    Исключение, которое выбрасывается, если переданный текст не является русским.
    """

    def __init__(self, message="Переданный текст не является русским."):
        self.message = message
        super().__init__(self.message)
