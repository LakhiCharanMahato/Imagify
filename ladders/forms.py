from django import forms
from .models import Ladder

class LadderForm(forms.ModelForm):
    class Meta:
        model=Ladder
        fields=['title','description','file']