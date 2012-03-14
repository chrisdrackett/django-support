from itertools import chain

from django import template
from django.conf import settings
from django.forms.widgets import RadioFieldRenderer
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

import html5 as forms

from support.functions import function_from_string

class ProfilePictureFieldRenderer(RadioFieldRenderer):
    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        t = template.loader.get_template('support/forms/profile_picture.html')
        return t.render(template.Context({'widget': self, 'MEDIA_URL': settings.MEDIA_URL }))

class ProfilePictureSelect(forms.RadioSelect):
    renderer = ProfilePictureFieldRenderer

class DateWidget(forms.DateInput):
    def render(self, name, value, attrs=None):
        t = template.loader.get_template('support/forms/date.html')
        c = template.Context({ 'name': name, 'value': value, 'widget': self })
        return t.render(c)

class LocationWidget(forms.TextInput):
    def __init__(self, attrs=None, choices=()):
        super(LocationWidget, self).__init__(attrs)
        self.choices = choices
    
    def value_from_datadict(self, data, files, name):
        l = data.get(name, None)
        if l:
            lat, lng = l.split(';')
            
            location = function_from_string(settings.GET_CREATE_LOCATION_FUNCTION)(lat, lng)
            if location:
                return location.pk
            else:
                return None
        else:
            return None;
    
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            location = None
            value = None
        else:
            location = value
            value = u"%s;%s" % (value.latitude, value.longitude)
    
        t = template.loader.get_template('support/forms/location.html')
        c = template.Context({ 'name': name, 'location': location, 'value': value, 'MEDIA_URL': settings.MEDIA_URL })
        return t.render(c)

class Select(forms.Widget):
    def __init__(self, attrs=None, choices=()):
        super(Select, self).__init__(attrs)
        self.choices = choices
    
    def render(self, name, value, attrs=None, choices=()):
        try:
            if value is None: value = self.choices[0][0]
        except TypeError:
            # when no choice exists
            pass
        
        selected = dict(self.choices).get(value)
        t = template.loader.get_template('support/forms/select.html')
        c = template.Context({ 'name': name, 'value': value, 'choices': self.choices, 'selected': selected })
        return t.render(c)

class ButtonSelect(forms.Widget):
    def __init__(self, attrs=None, choices=()):
        super(ButtonSelect, self).__init__(attrs)
        self.choices = choices

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        selected = dict(self.choices).get(value)
        t = template.loader.get_template('support/forms/button_select.html')
        c = template.Context({ 'name': name, 'value': value, 'choices': self.choices, 'selected': selected })
        return t.render(c)

class TokenInput(forms.TextInput):
    def __init__(self, attrs=None, callback_url=None):
        super(TokenInput, self).__init__(attrs=attrs)
        self.callback_url = callback_url
    
    def render(self, name, value, attrs=None):
        t = template.loader.get_template('support/forms/token_field.html')
        c = template.Context({ 'name': name, 'value': value, 'callback_url': self.callback_url })
        return t.render(c)

class CurrencyInput(forms.TextInput):
    def render(self, name, value, attrs=None):
        t = template.loader.get_template('support/forms/currency_field.html')
        if value is None:
            value = ''
        c = template.Context({ 'name': name, 'value': value })
        return t.render(c)

class CheckboxInput(forms.CheckboxInput):
    def render(self, name, value, attrs=None, custom_label=''):
        t = template.loader.get_template('support/forms/checkbox.html')
        
        if 'custom_label' in self.attrs:
            custom_label = self.attrs['custom_label']
        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
        try:
            checked = self.check_test(value)
        except: # Silently catch exceptions
            checked = False
        if value not in ('', True, False, None):
            # Only add the 'value' attribute if a value is non-empty.
            value = force_unicode(value)
        c = template.Context({ 'name': name, 'value': value, 'checked':checked, 'custom_label':custom_label})
        return t.render(c)


class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        t = template.loader.get_template("support/forms/multi_checkbox.html")
        if value is None:
            value = []
        
        str_values = set([force_unicode(v) for v in value])
        
        checkboxes = []
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):

            value = force_unicode(option_value)
            checkboxes.append({
                "name": name,
                "value": value,
                "checked": value in str_values,
                "label": conditional_escape(force_unicode(option_label)),
                "id": "id_%s_%s" % (name, i)
            })
        
        context = template.Context({
            "checkboxes": checkboxes,
            "name": name,
        })
        return t.render(context)
