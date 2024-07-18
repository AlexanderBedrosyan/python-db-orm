class CustomValidators:

    @staticmethod
    def validate_menu_categories(value):
        categories = ["Appetizers", "Main Course", "Desserts"]
        missing_categories = [category for category in categories if category not in value]
        if missing_categories:
            raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')
        return value


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        validators=[CustomValidators.validate_menu_categories]
    )
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE
    )