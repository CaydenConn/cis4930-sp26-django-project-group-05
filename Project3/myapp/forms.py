from django import forms
from django.core.exceptions import ValidationError
from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'name', 'rating', 'genre', 'year', 'released',
            'score', 'votes', 'director', 'writer', 'star',
            'country', 'budget', 'gross', 'company', 'runtime',
        ]
        widgets = {
            'name':     forms.TextInput(attrs={'class': 'form-control'}),
            'rating':   forms.Select(attrs={'class': 'form-select'}),
            'genre':    forms.Select(attrs={'class': 'form-select'}),
            'year':     forms.NumberInput(attrs={'class': 'form-control'}),
            'released': forms.TextInput(attrs={'class': 'form-control'}),
            'score':    forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'votes':    forms.NumberInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'writer':   forms.TextInput(attrs={'class': 'form-control'}),
            'star':     forms.TextInput(attrs={'class': 'form-control'}),
            'country':  forms.TextInput(attrs={'class': 'form-control'}),
            'budget':   forms.NumberInput(attrs={'class': 'form-control'}),
            'gross':    forms.NumberInput(attrs={'class': 'form-control'}),
            'company':  forms.TextInput(attrs={'class': 'form-control'}),
            'runtime':  forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
        }

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score is not None and not (0.0 <= score <= 10.0):
            raise ValidationError('Score must be between 0.0 and 10.0.')
        return score

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year is not None and not (1800 <= year <= 2030):
            raise ValidationError('Year must be between 1800 and 2030.')
        return year
