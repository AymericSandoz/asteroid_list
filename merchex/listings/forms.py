from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    start_date = forms.DateField(label='Date de début ',widget=DateInput)
    end_date = forms.DateField(label='Date de fin ',widget=DateInput)

  

