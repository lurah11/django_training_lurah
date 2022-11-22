from django import forms

class CalcForm (forms.Form): 
    f0_val = forms.FloatField()
    z_val = forms.FloatField()
    t_val = forms.FloatField()
    temp_val = forms.FloatField() 
    radio_calc = forms.CharField()
    re_val = forms.FloatField()