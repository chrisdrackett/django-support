# Default Django fields (to be subclassed below)
from django.forms import fields as django_fields
from django.forms.fields import *

# Support Custom Widgets
from support.forms import widgets as support_widgets
import widgets as html5_widgets

class IntegerField(django_fields.IntegerField):
    widget = html5_widgets.NumberInput
    
    def widget_attrs(self, widget):
        """
        Given a Widget instance (*not* a Widget class), returns a dictionary of
        any HTML attributes that should be added to the Widget, based on this
        Field.
        """
        attrs = {}
        if getattr(self, "min_value", None) is not None:
            attrs['min'] = self.min_value
        if getattr(self, "max_value", None) is not None:
            attrs['max'] = self.max_value
        return attrs

class CharField(django_fields.CharField):
    widget = html5_widgets.TextInput(attrs={'autocomplete':'off',})
    
    def __init__(self, max_length=100, *a, **kw):
        super(CharField, self).__init__(max_length=max_length, *a, **kw)

class ChoiceField(django_fields.ChoiceField):
    widget = support_widgets.Select

class TextField(django_fields.CharField):
    widget = html5_widgets.Textarea(attrs={'class':'autogrow', 'rows':2, 'cols':55})

class EmailField(django_fields.EmailField):
    widget = html5_widgets.EmailInput(attrs={'autocapitalize':'off', 'autocomplete':'off'})

class URLField(django_fields.URLField):
    widget = html5_widgets.URLInput

class TimeField(django_fields.TimeField):
    widget = html5_widgets.TimeInput

class DateField(django_fields.DateField):
    widget = support_widgets.DateWidget
    
    def __init__(self, *a, **kw):
        super(DateField, self).__init__(*a, **kw)

class DateTimeField(django_fields.DateTimeField):
    widget = html5_widgets.DateTimeInput
