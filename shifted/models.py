import os
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator,FileExtensionValidator

class RecipeName(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe_name = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # ForeignKey allows multiple RecipeNames per User
    desc = models.TextField(blank=True, null=True)
    duration = models.IntegerField(blank=True)

    class CuisineChoices(models.TextChoices):
        INDIAN = 'Indian', 'Indian'
        AMERICAN = 'American', 'American'
        CHINESE = 'Chinese', 'Chinese'
        JAPANESE = 'Japanese', 'Japanese'

    cuisine = models.CharField(max_length=10, choices=CuisineChoices.choices)

    def __str__(self):
        return self.recipe_name

class PatientDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-One relationship
    patient_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, null=True)
    age = models.PositiveIntegerField(default=55)
    gender = models.CharField(max_length=10, null=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    address = models.CharField(max_length=100, blank=True, null=True)
    phone_no = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    desc = models.TextField(blank=True, null=True, help_text="Provide details about You for consultant's reference.")

    def __str__(self):
        return f"{self.patient_id} - {self.user.username}"




class PatientProperty(models.Model):
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE)
    pp_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    occupation = models.CharField(max_length=20, default="Unemployed", blank=True, null=True)
    vhi_score = models.PositiveIntegerField(null=True, blank=True)
    rsi_score = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pp_id:
            self.pp_id = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pp_id} - {self.patient.user.username}"

    class SmokeChoices(models.TextChoices):
        SMOKER = '0', "SMOKER"
        NONSMOKER = '1', "NONSMOKER"

    class AlcoholChoices(models.TextChoices):
        HABITUAL_DRINKER = '1' , "HABITUAL DRINKER"
        CASUAL_DRINKER = '2', "CASUAL DRINKER"
        NONDRINKER = '3' , "NONDRINKER"

    class CarbonatedDrinksChoices(models.TextChoices):
        ALWAYS = '1' , "Always"
        ALMOST_ALWAYS = '2' , "Almost Always"
        SOMETIMES = '3' , "Sometimes"
        ALMOST_NEVER = '4' , 'Almost Never'
        NEVER = '5' , 'Never'

    class TomatoesChoices(models.TextChoices):
        ALMOST = '1', "Almost"
        ALWAYS = '2', "Always"
        SOMETIMES = '3', "Sometimes"
        NEVER = '4', "Never"

    smoker = models.CharField(max_length=10, choices=SmokeChoices.choices)
    cigar_per_day = models.PositiveIntegerField(null=True, blank=True)
    alcohol_consumption = models.CharField(
        max_length=1, 
        choices=AlcoholChoices.choices,
        default=AlcoholChoices.NONDRINKER
    )
    alcohol_quantity = models.PositiveIntegerField(null=True, blank=True)
    waters_quantity = models.PositiveIntegerField(null=True, blank=True)
    carbonated_drinks = models.CharField(
        max_length=1,
        choices=CarbonatedDrinksChoices.choices,
        default=CarbonatedDrinksChoices.SOMETIMES,
    )
    tomatoes = models.CharField(
        max_length=1,
        choices=TomatoesChoices.choices,
        default=TomatoesChoices.SOMETIMES,
    )

    # For getting details on the habits of coffee consumption.
    coffee = models.CharField(
        max_length=1,
        choices=CarbonatedDrinksChoices.choices,
        default=CarbonatedDrinksChoices.SOMETIMES,
    )
    coffee_quantity = models.PositiveIntegerField(null=True, blank=True)

    # Details on Chocolate consumption.
    chocolate = models.CharField(
        max_length=1,
        choices=CarbonatedDrinksChoices.choices,
        default=CarbonatedDrinksChoices.SOMETIMES,
    )
    chocolate_quantity = models.PositiveIntegerField(null=True, blank=True)

    # Cheese consumption details.
    soft_cheese = models.CharField(
        max_length=1,
        choices=CarbonatedDrinksChoices.choices,
        default=CarbonatedDrinksChoices.SOMETIMES,
    )
    cheese_quantity = models.PositiveIntegerField(null=True, blank=True)

    # Citrus Fruits consumption details.
    citrus_fruits = models.CharField(
        max_length=1,
        choices=CarbonatedDrinksChoices.choices,
        default=CarbonatedDrinksChoices.SOMETIMES,
    )
    citrus_fruits_quantity = models.PositiveIntegerField(null=True, blank=True)

    def clean(self):
        super().clean()
        # Define the choices that require a quantity field to be mandatory
        mandatory_choices_001 = [
            self.CarbonatedDrinksChoices.ALWAYS,
            self.CarbonatedDrinksChoices.ALMOST_ALWAYS,
            self.CarbonatedDrinksChoices.SOMETIMES,
            self.CarbonatedDrinksChoices.ALMOST_NEVER,
        ]


        # Validate coffee quantity
        if self.coffee in mandatory_choices_001 and self.coffee_quantity is None:
            raise ValidationError({'coffee_quantity': "This field is required for option chosen other than NEVER in Coffee."})

        # Validate chocolate quantity
        if self.chocolate in mandatory_choices_001 and self.chocolate_quantity is None:
            raise ValidationError({'chocolate_quantity': "This field is required for option chosen other than NEVER in Chocolate."})

        # Validate cheese quantity
        if self.soft_cheese in mandatory_choices_001 and self.cheese_quantity is None:
            raise ValidationError({'cheese_quantity': "This field is required for option chosen other than NEVER in Cheese."})

        # Validate citrus fruits quantity
        if self.citrus_fruits in mandatory_choices_001 and self.citrus_fruits_quantity is None:
            raise ValidationError({'citrus_fruits_quantity': "This field is required for option chosen other than NEVER in Citrus Fruits."})

        mandatory_choices_002 =[
            self.AlcoholChoices.CASUAL_DRINKER,
            self.AlcoholChoices.HABITUAL_DRINKER,
        ]

        # Validate alcohol_quantity
        if self.alcohol_consumption in mandatory_choices_002 and self.alcohol_quantity is None:
            raise ValidationError({'alcohol_quantity': "This field is required for option chosen other than NONDRINKER in Alcohol Consumption."})


        mandatory_choices_003 = [
            self.SmokeChoices.SMOKER,
        ]
        
        # Validate cigar_per_day
        if self.smoker in mandatory_choices_003 and self.cigar_per_day is None:
            raise ValidationError({'cigar_per_day': "This field is required for option chosen other than NONSMOKER in Cigar/day."})
    


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.wav', '.mp3', '.ogg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Unsupported file extension: {ext}.')

class AudioData(models.Model):

    def audio_file_path(instance, filename):
        ext = filename.split('.')[-1]
        return os.path.join('audio_files', f"{instance.audio_id}.{ext}")

    pp = models.ForeignKey(PatientProperty, on_delete=models.RESTRICT, default=None) 
    audio_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    audio_name = models.CharField(
        max_length=20,null = True, 
        blank=True, help_text="Provide a name")
    audio_file = models.FileField(
        upload_to=audio_file_path, 
        default=None,
        validators=[validate_file_extension],
        )
    predicted_condition = models.PositiveIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(6)])


    def __str__(self):
        return f"{self.pp.patient.user}-{self.audio_file.name[12:]}"