from support.forms import html5 as forms

def _get_meta_attr(attrs, attr, default):
    try:
        ret = getattr(attrs['Meta'], attr)
    except (KeyError, AttributeError):
        ret = default
    return ret

class SupportFormBaseMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['submit'] = _get_meta_attr(attrs, 'submit', 'Submit')
        attrs['no_submit'] = _get_meta_attr(attrs, 'no_submit', False)
        attrs['autofocus'] = _get_meta_attr(attrs, 'autofocus', False)
        attrs['labels'] = _get_meta_attr(attrs, 'labels', True)
        
        new_class = super(SupportFormBaseMetaclass, cls).__new__(cls, name, bases, attrs)
        return new_class

class FieldSetFormMetaclass(SupportFormBaseMetaclass, forms.forms.DeclarativeFieldsMetaclass):
    pass

class SupportBaseForm(forms.Form):
    __metaclass__ = FieldSetFormMetaclass

class SupportForm(SupportBaseForm):
    '''A subclass of django forms that gives us some flexability:
        
        * Ability to hide labels
        * Don't put ":" after labels
        * Add 'required' class to required elements
        * Auto focus initial element if auto-foucs is set in form definition
        
    '''
    def __init__(self, *args, **kwargs):
        super(SupportForm, self).__init__(*args, **kwargs)
        
        # Don't add a label suffix by default
        
        self.label_suffix = ''
        
        # Autofocus
        
        if self.autofocus:
            try:
                self.fields[self.fields.keys()[0]].widget.attrs.update({'autofocus': 'autofocus'})
            except AttributeError:
                # some fields can't be autofocused
                pass
        
        # Required Fields
        
        for field in self.fields:
            if self.fields[field].required:
                attrs = self.fields[field].widget.attrs
                klass = attrs.get('class', '').split(' ')
                if not 'required' in klass:
                    klass.append('required')
                    attrs.update({'class': ' '.join(klass)})
                    self.fields[field].widget.attrs = attrs
