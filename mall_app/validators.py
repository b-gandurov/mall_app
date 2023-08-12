from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(
        regex=r'^\d{1,15}$',
        message="Phone number must be entered in the format: '0888123456'. Up to 15 digits allowed."
    )