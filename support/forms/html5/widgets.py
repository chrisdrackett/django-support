"""
HTML5 input widgets.
TODO: Date widgets
"""
from django.forms.widgets import Input, Textarea

class HTML5Input(Input):
    def render(self, *args, **kwargs):
        return super(HTML5Input, self).render(*args, **kwargs)

class TextInput(HTML5Input):
    input_type = 'text'

class EmailInput(HTML5Input):
    input_type = 'email'
    
class URLInput(HTML5Input):
    input_type = 'url'

class SearchInput(HTML5Input):
    input_type = 'search'

class ColorInput(HTML5Input):
    input_type = 'color'
    
class NumberInput(HTML5Input):
    input_type = 'tel'
    
class RangeInput(NumberInput):
    input_type = 'range'
    
class DateInput(HTML5Input):
    input_type = 'date'
    
class MonthInput(HTML5Input):
    input_type = 'month'

class WeekInput(HTML5Input):
    input_type = 'week'

class TimeInput(HTML5Input):
    input_type = 'time'

class DateTimeInput(HTML5Input):
    input_type = 'datetime'

class DateTimeLocalInput(HTML5Input):
    input_type = 'datetime-local'
