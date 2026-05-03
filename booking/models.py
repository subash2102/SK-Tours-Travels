from django.core.validators import MinValueValidator
from django.db import models


class Car(models.Model):
    class Category(models.TextChoices):
        HATCHBACK = "HATCHBACK", "Hatchback"
        SEDAN = "SEDAN", "Sedan"
        SUV = "SUV", "SUV"
        MUV = "MUV", "MUV"
        MPV = "MPV", "MPV"
        LUXURY = "LUXURY", "Luxury"
        TEMPO = "TEMPO", "Tempo Traveller"

    class FuelType(models.TextChoices):
        PETROL = "PETROL", "Petrol"
        DIESEL = "DIESEL", "Diesel"
        CNG = "CNG", "CNG"
        EV = "EV", "EV"

    class Transmission(models.TextChoices):
        MANUAL = "MANUAL", "Manual"
        AUTOMATIC = "AUTOMATIC", "Automatic"

    name = models.CharField(max_length=120, help_text="Customer-facing name (e.g., Swift Dzire)")
    brand = models.CharField(max_length=80, blank=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.SEDAN)
    seats = models.PositiveIntegerField(default=4, validators=[MinValueValidator(1)])
    fuel_type = models.CharField(max_length=20, choices=FuelType.choices, default=FuelType.DIESEL)
    transmission = models.CharField(max_length=20, choices=Transmission.choices, default=Transmission.MANUAL)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to="cars/", blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_available", "category", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.seats} seats)"


class Driver(models.Model):
    full_name = models.CharField(max_length=120)
    photo = models.ImageField(upload_to="drivers/", blank=True, null=True)
    phone = models.CharField(max_length=20)
    experience_years = models.PositiveIntegerField(default=1)
    license_number = models.CharField(max_length=64)
    languages = models.CharField(max_length=120, blank=True, help_text="Comma-separated (e.g., English, Hindi, Tamil)")
    city = models.CharField(max_length=80, blank=True)
    is_available = models.BooleanField(default=True)
    assigned_car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name="drivers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_available", "-experience_years", "full_name"]

    def __str__(self) -> str:
        return self.full_name


class Booking(models.Model):
    class TripType(models.TextChoices):
        ONE_WAY = "ONE_WAY", "One-way"
        ROUND_TRIP = "ROUND_TRIP", "Round trip"
        LOCAL = "LOCAL", "Local"
        OUTSTATION = "OUTSTATION", "Outstation"

    class Status(models.TextChoices):
        NEW = "NEW", "New"
        CONTACTED = "CONTACTED", "Contacted"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    pickup_location = models.CharField(max_length=200)
    drop_location = models.CharField(max_length=200)
    pickup_datetime = models.DateTimeField()
    trip_type = models.CharField(max_length=20, choices=TripType.choices, default=TripType.ONE_WAY)
    passengers = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    notes = models.TextField(blank=True)

    preferred_car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")
    preferred_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.full_name} • {self.pickup_location} → {self.drop_location}"


class Review(models.Model):
    class Rating(models.IntegerChoices):
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"
        FIVE = 5, "5"

    customer_name = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(choices=Rating.choices, default=Rating.FIVE)
    message = models.TextField(max_length=600)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.customer_name} ({self.rating}/5)"
