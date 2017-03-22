from django import forms

from .models import Facemash


class FaceForm(forms.Form):
    winner = forms.IntegerField()
    loser = forms.IntegerField()

    def clean_winner(self):
        winner = self.cleaned_data['winner']
        try:
            return Facemash.objects.get(id=winner)
        except Facemash.DoesNotExist:
            raise forms.ValidationError('invalid form')

    def clean_loser(self):
        loser = self.cleaned_data['loser']
        try:
            return Facemash.objects.get(id=loser)
        except Facemash.DoesNotExist:
            raise forms.ValidationError('invalid form')


class FacemashUpdateForm(forms.ModelForm):

    class Meta(object):
        model = Facemash

        fields = (
            'photo',
        )

        widgets = {
            'photo': forms.FileInput(),
        }
