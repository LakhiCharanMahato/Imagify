from django import forms
from .models import Ladder

class LadderForm(forms.ModelForm):
    class Meta:
        model=Ladder
        fields=['title','description','file']

    def clean_file(self):
        cleaned_data=self.cleaned_data
        file=cleaned_data.get('file')

        if file.content_type not in ('video/mp4','image/jpeg','image/png'):
            self.add_error("file","Only allowed data types are jpg, jpeg, png and mp4")
        
        return file