from django import forms


class HashpanForm(forms.Form):
    first_six_letters = forms.CharField(
        min_length=6, max_length=6, help_text="Первые 6 цифр карты"
    )
    last_four_letters = forms.CharField(
        min_length=4, max_length=4, help_text="Последние 4 цифры карты"
    )
