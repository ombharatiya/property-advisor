from django import forms


class InputForm(forms.Form):

    lon = forms.DecimalField(max_digits=8, decimal_places=3)
    lat = forms.DecimalField(max_digits=8, decimal_places=3)
    min_budget = forms.DecimalField(
        max_digits=8, min_value=0.0, decimal_places=2)
    max_budget = forms.DecimalField(
        max_digits=8, min_value=0.0, decimal_places=2)
    min_bedrooms = forms.IntegerField(
        min_value=0,
        help_text="min bedrooms"
    )
    max_bedrooms = forms.IntegerField(
        min_value=0,
        help_text="max bedrooms"
    )
    min_bathrooms = forms.IntegerField(
        min_value=0,
        help_text="min bathrooms"
    )
    max_bathrooms = forms.IntegerField(
        min_value=0,
        help_text="max bathrooms"
    )
