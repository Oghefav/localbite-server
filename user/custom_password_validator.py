import re
from django.core.exceptions import ValidationError
class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError('password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', password):
            raise ValidationError('password must contain at least one lowercase letter')
        if not re.search(r'\d', password):
            raise ValidationError('password must contain at least a digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('password must contain at least a character')
        
    def get_help_text(self):
        return "Your password must contain at least one uppercase, one lowercase, one digit, and one special character."
    

    # r'[!@#$%^&*(),.?":\\{}|<>]'