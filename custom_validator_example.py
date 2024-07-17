from django.core.exceptions import ValidationError


class VideoGameValidator:

    def __init__(self, min_rating: float, max_rating: float, message=None):
        self.min_rating = min_rating
        self.max_rating = max_rating
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value:
            self.__message = value
        else:
            self.__message = "The rating must be between 0.0 and 10.0"

    def __call__(self, value):
        if not (self.min_rating <= value <= self.max_rating):
            raise ValidationError(self.message)

    def deconstruct(self):
        return (
            f'main_app.validators.VideoGameValidator',  # Пътят към класа
            (self.min_rating, self.max_rating),  # Позиционните аргументи
            {'message': self.message},  # Ключовите аргументи
            {}  # Допълнителни опции
        )
