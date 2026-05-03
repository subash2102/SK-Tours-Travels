from django.conf import settings
from django.core.mail import send_mail


def send_booking_status_email(booking) -> tuple[bool, str]:
    recipient_email = (booking.email or "").strip()
    if not recipient_email:
        return False, "Customer email is missing."

    subject = f"Booking Status Update - {booking.get_status_display()}"
    pickup_time = booking.pickup_datetime.strftime("%d %b %Y, %I:%M %p")
    admin_phone = getattr(settings, "ADMIN_PHONE_NUMBER", "").strip()
    contact_line = (
        f"If you need any help, please reply to this email or call us at {admin_phone}.\n\n"
        if admin_phone
        else "If you need any help, please reply to this email or contact SK Tours & Travels.\n\n"
    )
    body = (
        f"Hello {booking.full_name},\n\n"
        f"Your booking status is now: {booking.get_status_display()}.\n\n"
        f"Trip Details:\n"
        f"- Pickup: {booking.pickup_location}\n"
        f"- Drop: {booking.drop_location}\n"
        f"- Date & Time: {pickup_time}\n"
        f"- Trip Type: {booking.get_trip_type_display()}\n\n"
        f"{contact_line}"
        "Regards,\n"
        "SK Tours & Travels"
    )

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "")
    if not from_email:
        return False, "DEFAULT_FROM_EMAIL is not configured."

    sent_count = send_mail(
        subject=subject,
        message=body,
        from_email=from_email,
        recipient_list=[recipient_email],
        fail_silently=False,
    )
    return (sent_count > 0, "Email sent." if sent_count > 0 else "Email not sent.")
