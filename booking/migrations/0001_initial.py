# Generated manually for this starter project.
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Car",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="Customer-facing name (e.g., Swift Dzire)", max_length=120)),
                ("brand", models.CharField(blank=True, max_length=80)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("HATCHBACK", "Hatchback"),
                            ("SEDAN", "Sedan"),
                            ("SUV", "SUV"),
                            ("MUV", "MUV"),
                            ("LUXURY", "Luxury"),
                            ("TEMPO", "Tempo Traveller"),
                        ],
                        default="SEDAN",
                        max_length=20,
                    ),
                ),
                (
                    "seats",
                    models.PositiveIntegerField(
                        default=4,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                (
                    "fuel_type",
                    models.CharField(
                        choices=[("PETROL", "Petrol"), ("DIESEL", "Diesel"), ("CNG", "CNG"), ("EV", "EV")],
                        default="DIESEL",
                        max_length=20,
                    ),
                ),
                (
                    "transmission",
                    models.CharField(
                        choices=[("MANUAL", "Manual"), ("AUTOMATIC", "Automatic")],
                        default="MANUAL",
                        max_length=20,
                    ),
                ),
                ("price_per_km", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("price_per_day", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("description", models.TextField(blank=True)),
                ("main_image", models.ImageField(blank=True, null=True, upload_to="cars/")),
                ("is_available", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-is_available", "category", "name"]},
        ),
        migrations.CreateModel(
            name="Driver",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120)),
                ("photo", models.ImageField(blank=True, null=True, upload_to="drivers/")),
                ("phone", models.CharField(max_length=20)),
                ("experience_years", models.PositiveIntegerField(default=1)),
                ("license_number", models.CharField(max_length=64)),
                (
                    "languages",
                    models.CharField(
                        blank=True,
                        help_text="Comma-separated (e.g., English, Hindi, Tamil)",
                        max_length=120,
                    ),
                ),
                ("city", models.CharField(blank=True, max_length=80)),
                ("is_available", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "assigned_car",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="drivers",
                        to="booking.car",
                    ),
                ),
            ],
            options={"ordering": ["-is_available", "-experience_years", "full_name"]},
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=20)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("pickup_location", models.CharField(max_length=200)),
                ("drop_location", models.CharField(max_length=200)),
                ("pickup_datetime", models.DateTimeField()),
                (
                    "trip_type",
                    models.CharField(
                        choices=[
                            ("ONE_WAY", "One-way"),
                            ("ROUND_TRIP", "Round trip"),
                            ("LOCAL", "Local"),
                            ("OUTSTATION", "Outstation"),
                        ],
                        default="ONE_WAY",
                        max_length=20,
                    ),
                ),
                (
                    "passengers",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NEW", "New"),
                            ("CONTACTED", "Contacted"),
                            ("CONFIRMED", "Confirmed"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="NEW",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "preferred_car",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="bookings",
                        to="booking.car",
                    ),
                ),
                (
                    "preferred_driver",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="bookings",
                        to="booking.driver",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]

