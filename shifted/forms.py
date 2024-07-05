# from django.forms import ModelForm
from django import forms
# from django.core.exceptions import ValidationError
from .models import RecipeName, AudioData, PatientDetail, PatientProperty

class Post_Recipes(forms.ModelForm):
    class Meta:
        model = RecipeName
        fields = ['recipe_name', 'desc', 'duration', 'cuisine']
        # form = ['RecipeName', "Desc"]

class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientDetail
        exclude = ['user', 'patient_id']

class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = AudioData
        fields = ['audio_file','audio_name']

class PatientPropertiesForm(forms.ModelForm):
    class Meta:
        model = PatientProperty
        exclude  = ['patient','pp_id','timestamp']  # Or list the specific fields you want to include

    def clean(self):
        cleaned_data = super().clean()
        
        coffee = cleaned_data.get('coffee')
        coffee_quantity = cleaned_data.get('coffee_quantity')
        chocolate = cleaned_data.get('chocolate')
        chocolate_quantity = cleaned_data.get('chocolate_quantity')
        soft_cheese = cleaned_data.get('soft_cheese')
        cheese_quantity = cleaned_data.get('cheese_quantity')
        citrus_fruits = cleaned_data.get('citrus_fruits')
        citrus_fruits_quantity = cleaned_data.get('citrus_fruits_quantity')

        mandatory_choices = [
            PatientProperty.CarbonatedDrinksChoices.ALWAYS,
            PatientProperty.CarbonatedDrinksChoices.ALMOST_ALWAYS,
            PatientProperty.CarbonatedDrinksChoices.SOMETIMES,
            PatientProperty.CarbonatedDrinksChoices.ALMOST_NEVER,
        ]

        # Validate coffee quantity
        if coffee in mandatory_choices and coffee_quantity is None:
            self.add_error('coffee_quantity', "This field is required for selected coffee choice.")

        # Validate chocolate quantity
        if chocolate in mandatory_choices and chocolate_quantity is None:
            self.add_error('chocolate_quantity', "This field is required for selected chocolate choice.")

        # Validate cheese quantity
        if soft_cheese in mandatory_choices and cheese_quantity is None:
            self.add_error('cheese_quantity', "This field is required for selected cheese choice.")

        # Validate citrus fruits quantity
        if citrus_fruits in mandatory_choices and citrus_fruits_quantity is None:
            self.add_error('citrus_fruits_quantity', "This field is required for selected citrus fruits choice.")
        
        return cleaned_data