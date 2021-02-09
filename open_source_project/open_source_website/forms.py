
from django import forms


class emailsForNewsletter(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required': True,
                                                            "size": 40}))


class contactForm(forms.Form):
    email = forms.EmailField(initial="Mail:",
                             widget=forms.EmailInput(attrs={'required': True,
                                                            "size": 40}))
    sujet = forms.CharField(initial="Sujet:",
                            widget=forms.TextInput(attrs={'required': True,
                                                          'size': 40}))

    message = forms.CharField(widget=forms.Textarea(attrs={'required': True,
                                                           'cols': '40', 'rows': '7'}))

