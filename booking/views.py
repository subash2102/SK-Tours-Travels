from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .decorators import staff_required
from .forms import BookingForm, BookingStatusForm, CarForm, DriverForm, ReviewForm
from .models import Booking, Car, Driver, Review
from .notifications import send_booking_status_email


def home(request):
    cars = Car.objects.filter(is_available=True)[:6]
    drivers = Driver.objects.filter(is_available=True)[:6]
    reviews = Review.objects.filter(is_approved=True)[:6]
    review_form = ReviewForm()
    return render(
        request,
        "public/home.html",
        {"featured_cars": cars, "featured_drivers": drivers, "reviews": reviews, "review_form": review_form},
    )


def submit_review(request):
    if request.method != "POST":
        raise Http404
    form = ReviewForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Thanks! Your feedback was submitted for approval.")
    else:
        messages.error(request, "Please correct the feedback form and try again.")
    return redirect("home")


def cars_list(request):
    qs = Car.objects.all()
    q = (request.GET.get("q") or "").strip()
    category = (request.GET.get("category") or "").strip()
    seats = (request.GET.get("seats") or "").strip()

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(brand__icontains=q) | Q(description__icontains=q))
    if category:
        qs = qs.filter(category=category)
    if seats.isdigit():
        qs = qs.filter(seats=int(seats))

    return render(
        request,
        "public/cars_list.html",
        {
            "cars": qs,
            "q": q,
            "category": category,
            "seats": seats,
            "categories": Car.Category.choices,
        },
    )


def car_detail(request, pk: int):
    car = get_object_or_404(Car, pk=pk)
    return render(request, "public/car_detail.html", {"car": car})


def drivers_list(request):
    qs = Driver.objects.all()
    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(
            Q(full_name__icontains=q)
            | Q(languages__icontains=q)
            | Q(city__icontains=q)
            | Q(license_number__icontains=q)
        )
    return render(request, "public/drivers_list.html", {"drivers": qs, "q": q})


def driver_detail(request, pk: int):
    driver = get_object_or_404(Driver, pk=pk)
    return render(request, "public/driver_detail.html", {"driver": driver})


def book(request):
    initial = {}
    car_id = request.GET.get("car")
    driver_id = request.GET.get("driver")
    if car_id and car_id.isdigit():
        initial["preferred_car"] = Car.objects.filter(pk=int(car_id)).first()
    if driver_id and driver_id.isdigit():
        initial["preferred_driver"] = Driver.objects.filter(pk=int(driver_id)).first()

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your enquiry has been received. We'll contact you shortly.")
            return redirect("book_success")
        messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm(initial=initial)

    return render(request, "public/book.html", {"form": form})


def book_success(request):
    return render(request, "public/book_success.html")


@staff_required
def dashboard_home(request):
    return render(
        request,
        "dashboard/home.html",
        {
            "cars_count": Car.objects.count(),
            "drivers_count": Driver.objects.count(),
            "bookings_count": Booking.objects.count(),
            "new_bookings_count": Booking.objects.filter(status=Booking.Status.NEW).count(),
        },
    )


@staff_required
def dashboard_cars(request):
    q = (request.GET.get("q") or "").strip()
    qs = Car.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(brand__icontains=q))
    return render(request, "dashboard/cars_list.html", {"cars": qs, "q": q})


@staff_required
def dashboard_car_create(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Car added.")
            return redirect("dashboard_cars")
        messages.error(request, "Please correct the errors below.")
    else:
        form = CarForm()
    return render(request, "dashboard/car_form.html", {"form": form, "mode": "create"})


@staff_required
def dashboard_car_edit(request, pk: int):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Car updated.")
            return redirect("dashboard_cars")
        messages.error(request, "Please correct the errors below.")
    else:
        form = CarForm(instance=car)
    return render(request, "dashboard/car_form.html", {"form": form, "mode": "edit", "car": car})


@staff_required
def dashboard_car_delete(request, pk: int):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        car.delete()
        messages.success(request, "Car deleted.")
        return redirect("dashboard_cars")
    return render(request, "dashboard/confirm_delete.html", {"object": car, "cancel_url": reverse("dashboard_cars")})


@staff_required
def dashboard_drivers(request):
    q = (request.GET.get("q") or "").strip()
    qs = Driver.objects.select_related("assigned_car").all()
    if q:
        qs = qs.filter(Q(full_name__icontains=q) | Q(city__icontains=q) | Q(languages__icontains=q))
    return render(request, "dashboard/drivers_list.html", {"drivers": qs, "q": q})


@staff_required
def dashboard_driver_create(request):
    if request.method == "POST":
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver added.")
            return redirect("dashboard_drivers")
        messages.error(request, "Please correct the errors below.")
    else:
        form = DriverForm()
    return render(request, "dashboard/driver_form.html", {"form": form, "mode": "create"})


@staff_required
def dashboard_driver_edit(request, pk: int):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == "POST":
        form = DriverForm(request.POST, request.FILES, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver updated.")
            return redirect("dashboard_drivers")
        messages.error(request, "Please correct the errors below.")
    else:
        form = DriverForm(instance=driver)
    return render(request, "dashboard/driver_form.html", {"form": form, "mode": "edit", "driver": driver})


@staff_required
def dashboard_driver_delete(request, pk: int):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == "POST":
        driver.delete()
        messages.success(request, "Driver deleted.")
        return redirect("dashboard_drivers")
    return render(
        request,
        "dashboard/confirm_delete.html",
        {"object": driver, "cancel_url": reverse("dashboard_drivers")},
    )


@staff_required
def dashboard_bookings(request):
    q = (request.GET.get("q") or "").strip()
    status = (request.GET.get("status") or "").strip()

    qs = Booking.objects.select_related("preferred_car", "preferred_driver").all()
    if q:
        qs = qs.filter(
            Q(full_name__icontains=q)
            | Q(phone__icontains=q)
            | Q(pickup_location__icontains=q)
            | Q(drop_location__icontains=q)
        )
    if status:
        qs = qs.filter(status=status)

    return render(
        request,
        "dashboard/bookings_list.html",
        {"bookings": qs, "q": q, "status": status, "statuses": Booking.Status.choices},
    )


@staff_required
def dashboard_booking_detail(request, pk: int):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == "POST":
        previous_status = booking.status
        form = BookingStatusForm(request.POST, instance=booking)
        if form.is_valid():
            updated_booking = form.save()
            if previous_status != updated_booking.status:
                sent, details = send_booking_status_email(updated_booking)
                if sent:
                    messages.success(request, "Booking updated and status email sent.")
                else:
                    messages.warning(request, f"Booking updated, but status email was not sent: {details}")
            else:
                messages.success(request, "Booking updated.")
            return redirect("dashboard_booking_detail", pk=booking.pk)
        messages.error(request, "Please correct the errors below.")
    else:
        form = BookingStatusForm(instance=booking)
    
    from booking.whatsapp import build_booking_whatsapp_url
    whatsapp_message_url = build_booking_whatsapp_url(booking)
    
    return render(request, "dashboard/booking_detail.html", {
        "booking": booking,
        "form": form,
        "whatsapp_message_url": whatsapp_message_url,
    })


@staff_required
def dashboard_reviews(request):
    status = (request.GET.get("status") or "pending").strip()
    qs = Review.objects.all()
    if status == "approved":
        qs = qs.filter(is_approved=True)
    elif status == "pending":
        qs = qs.filter(is_approved=False)
    return render(request, "dashboard/reviews_list.html", {"reviews": qs, "status": status})


@staff_required
def dashboard_review_toggle(request, pk: int):
    if request.method != "POST":
        raise Http404
    review = get_object_or_404(Review, pk=pk)
    review.is_approved = not review.is_approved
    review.save(update_fields=["is_approved"])
    messages.success(request, "Review updated.")
    return redirect("dashboard_reviews")


@staff_required
def dashboard_review_delete(request, pk: int):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        review.delete()
        messages.success(request, "Review deleted.")
        return redirect("dashboard_reviews")
    return render(
        request,
        "dashboard/confirm_delete.html",
        {"object": review, "cancel_url": reverse("dashboard_reviews")},
    )

