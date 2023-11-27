from django import forms
from .models import Profile


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    verify_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()

        # cleaned_data['email'] = cleaned_data.get('email').lower()
        # cleaned_data['verify_email'] = cleaned_data.get('verify_email').lower()

        if cleaned_data.get('email') != cleaned_data.get('verify_email'):
            self.add_error('email', 'Emails do not match')
        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
