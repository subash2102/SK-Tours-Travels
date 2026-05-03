from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("reviews/submit/", views.submit_review, name="submit_review"),
    path("cars/", views.cars_list, name="cars_list"),
    path("cars/<int:pk>/", views.car_detail, name="car_detail"),
    path("drivers/", views.drivers_list, name="drivers_list"),
    path("drivers/<int:pk>/", views.driver_detail, name="driver_detail"),
    path("book/", views.book, name="book"),
    path("book/success/", views.book_success, name="book_success"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="auth/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Custom admin dashboard
    path("dashboard/", views.dashboard_home, name="dashboard_home"),
    path("dashboard/cars/", views.dashboard_cars, name="dashboard_cars"),
    path("dashboard/cars/new/", views.dashboard_car_create, name="dashboard_car_create"),
    path("dashboard/cars/<int:pk>/edit/", views.dashboard_car_edit, name="dashboard_car_edit"),
    path("dashboard/cars/<int:pk>/delete/", views.dashboard_car_delete, name="dashboard_car_delete"),
    path("dashboard/drivers/", views.dashboard_drivers, name="dashboard_drivers"),
    path("dashboard/drivers/new/", views.dashboard_driver_create, name="dashboard_driver_create"),
    path("dashboard/drivers/<int:pk>/edit/", views.dashboard_driver_edit, name="dashboard_driver_edit"),
    path("dashboard/drivers/<int:pk>/delete/", views.dashboard_driver_delete, name="dashboard_driver_delete"),
    path("dashboard/bookings/", views.dashboard_bookings, name="dashboard_bookings"),
    path("dashboard/bookings/<int:pk>/", views.dashboard_booking_detail, name="dashboard_booking_detail"),
    path("dashboard/reviews/", views.dashboard_reviews, name="dashboard_reviews"),
    path("dashboard/reviews/<int:pk>/toggle/", views.dashboard_review_toggle, name="dashboard_review_toggle"),
    path("dashboard/reviews/<int:pk>/delete/", views.dashboard_review_delete, name="dashboard_review_delete"),
]
