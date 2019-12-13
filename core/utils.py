from django.db import models
from django.core import validators

class HtmlColorCodeField(models.CharField):
    """
    A CharField that checks that the value is a valid HTML color code (Hex triplet).
    Has no required argument.
    
    """
    def __init__(self, **kwargs):
        kwargs['max_length'] = 7
        validator_list = kwargs.get('validators', [])
        validator_list.append(HtmlColorCodeField.is_html_color_code)
        kwargs['validators'] = validator_list
        super(HtmlColorCodeField,self).__init__(**kwargs)
        
    def get_internal_type(self):
        return "CharField"
    
    @staticmethod    
    def is_html_color_code(field_data, all_data):
        """
        Checks that field_data is a HTML color code string.
        
        """
        try:
            if not field_data.startswith("#") or not field_data[1:].isalnum() or not len(field_data) == 7:
                raise validators.ValidationError("Please enter a valid HTML color.")
        except (TypeError, ValueError) as e:
            raise validators.ValidationError(str(e))
    
    def validate(self, value, all_values):
        HtmlColorCodeField.is_html_color_code(value, all_values)