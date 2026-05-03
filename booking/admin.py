from django.contrib import admin

from .models import Booking, Car, Driver, Review


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "seats", "fuel_type", "transmission", "is_available", "created_at")
    list_filter = ("category", "fuel_type", "transmission", "is_available")
    search_fields = ("name", "brand", "description")


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("full_name", "city", "experience_years", "is_available", "assigned_car", "created_at")
    list_filter = ("is_available", "city")
    search_fields = ("full_name", "languages", "license_number", "phone")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "pickup_location", "drop_location", "pickup_datetime", "status", "created_at")
    list_filter = ("status", "trip_type")
    search_fields = ("full_name", "phone", "email", "pickup_location", "drop_location")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "rating")
    search_fields = ("customer_name", "message")
