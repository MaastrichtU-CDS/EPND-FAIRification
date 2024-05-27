from django import forms


class CSVUploadForm(forms.Form):
    file = forms.FileField()
