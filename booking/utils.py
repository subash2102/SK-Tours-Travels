from urllib.parse import quote

from .whatsapp import _normalize_phone


def build_booking_whatsapp_url(booking) -> str:
    """
    Build a wa.me click-to-chat URL for a booking.
    Returns the full WhatsApp link with pre-filled message.
    """
    phone = _normalize_phone(getattr(booking, "phone", ""))
    if not phone:
        return ""
    
    # Remove the + prefix for wa.me URL
    phone_without_plus = phone.lstrip("+")
    
    status_label = booking.get_status_display()
    pickup_time = booking.pickup_datetime.strftime("%d %b %Y, %I:%M %p")
    message = (
        f"Hello {booking.full_name}\n\n"
        f"Your booking status is: {status_label}\n\n"
        f"Pickup: {booking.pickup_location}\n"
        f"Drop: {booking.drop_location}\n"
        f"Date: {pickup_time}\n\n"
        f"Thank you for choosing SK Tours & Travels."
    )
    
    encoded_message = quote(message)
    return f"https://wa.me/{phone_without_plus}?text={encoded_message}"
