from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.add_input(Submit('submit', 'Envoyer', css_class='btn-primary'))
        self.helper.layout = Layout(
            FloatingField('recipient'),
            FloatingField('subject'),
            Field('content', css_class='form-control'),
        ) 