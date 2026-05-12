import json
import logging
from urllib import error, request

from django.conf import settings


logger = logging.getLogger(__name__)


def _normalize_phone(raw_phone: str) -> str:
    raw = (raw_phone or "").strip()
    if not raw:
        return ""

    allowed = "".join(ch for ch in raw if ch.isdigit() or ch == "+")
    if allowed.startswith("+"):
        return allowed
    if allowed.startswith("00"):
        return f"+{allowed[2:]}"

    default_country_code = getattr(settings, "WHATSAPP_DEFAULT_COUNTRY_CODE", "+91")
    digits = "".join(ch for ch in allowed if ch.isdigit())
    if len(digits) == 10 and default_country_code:
        return f"{default_country_code}{digits}"
    return f"+{digits}" if digits else ""


def send_booking_status_whatsapp(booking) -> tuple[bool, str]:
    """
    Send a plain-text WhatsApp status update via Meta WhatsApp Cloud API.
    Returns (success, details_or_error).
    """
    if not getattr(settings, "WHATSAPP_ENABLED", False):
        return False, "WhatsApp integration is disabled."

    phone_number_id = getattr(settings, "WHATSAPP_PHONE_NUMBER_ID", "")
    access_token = getattr(settings, "WHATSAPP_ACCESS_TOKEN", "")
    api_version = getattr(settings, "WHATSAPP_API_VERSION", "v21.0")

    if not phone_number_id or not access_token:
        return False, "WhatsApp credentials are missing."

    recipient_phone = _normalize_phone(getattr(booking, "phone", ""))
    if not recipient_phone:
        return False, "Customer phone number is invalid."

    status_label = booking.get_status_display()
    pickup_time = booking.pickup_datetime.strftime("%d %b %Y, %I:%M %p")
    message_text = (
        f"Hello {booking.full_name}, your booking status is now: {status_label}.\n"
        f"Trip: {booking.pickup_location} to {booking.drop_location}\n"
        f"Pickup: {pickup_time}\n"
        "For help, reply to this message or contact SK Tours & Travels."
    )

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_phone,
        "type": "text",
        "text": {"body": message_text},
    }

    endpoint = f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages"
    req = request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )

    try:
        with request.urlopen(req, timeout=15) as response:
            body = response.read().decode("utf-8")
            return True, body
    except error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        logger.warning("WhatsApp send failed with HTTP %s: %s", exc.code, err_body)
        return False, f"HTTP {exc.code}: {err_body}"
    except Exception as exc:  # pragma: no cover
        logger.exception("WhatsApp send failed")
        return False, str(exc)


def build_booking_whatsapp_url(booking) -> str:
    """
    Build a wa.me click-to-chat URL for a booking.
    Returns the full WhatsApp link with pre-filled message.
    """
    from urllib.parse import quote
    
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
