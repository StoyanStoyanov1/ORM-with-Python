from django.core.exceptions import ValidationError


def validator_rating(value):
    if value not in range(0, 11):
        raise ValidationError("The rating must be between 0.0 and 10.0")

    return value


def validator_release_year(value):
    if value not in range(1990, 2024):
        raise ValidationError("The release year must be between 1990 and 2023")

    return value
