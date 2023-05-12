from django.core.validators import RegexValidator


class UsernameValidator(RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = 'Enter a valid username.'