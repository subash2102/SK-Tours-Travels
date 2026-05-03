from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from booking.models import Booking, Car, Driver, Review


class Command(BaseCommand):
    help = "Seed demo cars, drivers, and a few bookings."

    def handle(self, *args, **options):
        cars = [
            Car(
                name="Swift Dzire",
                brand="Maruti Suzuki",
                category=Car.Category.SEDAN,
                seats=4,
                fuel_type=Car.FuelType.DIESEL,
                transmission=Car.Transmission.MANUAL,
                price_per_km="14.00",
                description="Comfortable sedan for city rides and airport drops.",
                is_available=True,
            ),
            Car(
                name="Innova Crysta",
                brand="Toyota",
                category=Car.Category.MUV,
                seats=7,
                fuel_type=Car.FuelType.DIESEL,
                transmission=Car.Transmission.MANUAL,
                price_per_day="4500.00",
                description="Spacious MUV ideal for family trips and outstation travel.",
                is_available=True,
            ),
            Car(
                name="Ertiga",
                brand="Maruti Suzuki",
                category=Car.Category.MUV,
                seats=7,
                fuel_type=Car.FuelType.PETROL,
                transmission=Car.Transmission.MANUAL,
                price_per_km="18.00",
                description="Practical 7-seater with great mileage.",
                is_available=True,
            ),
            Car(
                name="Tempo Traveller (12 Seater)",
                brand="Force",
                category=Car.Category.TEMPO,
                seats=12,
                fuel_type=Car.FuelType.DIESEL,
                transmission=Car.Transmission.MANUAL,
                price_per_day="6500.00",
                description="Group travel made easy with comfortable seating.",
                is_available=True,
            ),
        ]

        created_cars = []
        for c in cars:
            obj, _ = Car.objects.get_or_create(
                name=c.name,
                defaults={
                    "brand": c.brand,
                    "category": c.category,
                    "seats": c.seats,
                    "fuel_type": c.fuel_type,
                    "transmission": c.transmission,
                    "price_per_km": c.price_per_km,
                    "price_per_day": c.price_per_day,
                    "description": c.description,
                    "is_available": c.is_available,
                },
            )
            created_cars.append(obj)

        drivers = [
            Driver(
                full_name="Ravi Kumar",
                phone="9XXXXXXXX1",
                experience_years=6,
                license_number="TN-XXXX-123456",
                languages="English, Hindi, Tamil",
                city="Chennai",
                is_available=True,
                assigned_car=created_cars[0],
            ),
            Driver(
                full_name="Suresh Singh",
                phone="9XXXXXXXX2",
                experience_years=9,
                license_number="TN-XXXX-234567",
                languages="Hindi, English",
                city="Chennai",
                is_available=True,
                assigned_car=created_cars[1],
            ),
            Driver(
                full_name="Imran Ali",
                phone="9XXXXXXXX3",
                experience_years=4,
                license_number="TN-XXXX-345678",
                languages="English, Tamil",
                city="Chennai",
                is_available=True,
                assigned_car=None,
            ),
        ]

        created_drivers = []
        for d in drivers:
            obj, _ = Driver.objects.get_or_create(
                full_name=d.full_name,
                defaults={
                    "phone": d.phone,
                    "experience_years": d.experience_years,
                    "license_number": d.license_number,
                    "languages": d.languages,
                    "city": d.city,
                    "is_available": d.is_available,
                    "assigned_car": d.assigned_car,
                },
            )
            created_drivers.append(obj)

        if not Booking.objects.exists():
            now = timezone.now()
            Booking.objects.create(
                full_name="Demo Customer",
                phone="9XXXXXXXX9",
                email="demo@example.com",
                pickup_location="Chennai Airport",
                drop_location="T Nagar",
                pickup_datetime=now + timedelta(days=1),
                trip_type=Booking.TripType.ONE_WAY,
                passengers=2,
                preferred_car=created_cars[0],
                preferred_driver=created_drivers[0],
                notes="Please call 10 minutes before arrival.",
            )

        if not Review.objects.exists():
            Review.objects.create(customer_name="Anita", rating=5, message="Driver arrived early, car was clean, and the ride was smooth.", is_approved=True)
            Review.objects.create(customer_name="Rahul", rating=5, message="Transparent pricing and quick confirmation. Great experience for our family trip.", is_approved=True)
            Review.objects.create(customer_name="Sahana", rating=5, message="Polite driver, good route knowledge, and very comfortable ride.", is_approved=True)

        self.stdout.write(self.style.SUCCESS("Seed complete: cars, drivers, bookings."))
