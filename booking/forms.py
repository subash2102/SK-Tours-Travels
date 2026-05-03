from django import forms
from django.utils import timezone

from .models import Booking, Car, Driver, Review


class BookingForm(forms.ModelForm):
    preferred_car = forms.ModelChoiceField(queryset=Car.objects.none(), required=False, empty_label="No preference")
    preferred_driver = forms.ModelChoiceField(queryset=Driver.objects.none(), required=False, empty_label="No preference")

    class Meta:
        model = Booking
        fields = [
            "full_name",
            "phone",
            "email",
            "pickup_location",
            "drop_location",
            "pickup_datetime",
            "trip_type",
            "passengers",
            "preferred_car",
            "preferred_driver",
            "notes",
        ]
        widgets = {
            "pickup_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_pickup_datetime(self):
        dt = self.cleaned_data["pickup_datetime"]
        if dt < timezone.now():
            raise forms.ValidationError("Pickup date/time must be in the future.")
        return dt

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["preferred_car"].queryset = Car.objects.filter(is_available=True).order_by("category", "name")
        self.fields["preferred_driver"].queryset = Driver.objects.filter(is_available=True).order_by("-experience_years", "full_name")
        self.fields["email"].required = True
        self.fields["email"].widget.attrs["required"] = "required"


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "name",
            "brand",
            "category",
            "seats",
            "fuel_type",
            "transmission",
            "price_per_km",
            "price_per_day",
            "description",
            "main_image",
            "is_available",
        ]


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            "full_name",
            "photo",
            "phone",
            "experience_years",
            "license_number",
            "languages",
            "city",
            "is_available",
            "assigned_car",
        ]


class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["status"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["customer_name", "rating", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 4, "placeholder": "Share your experience..."})}
