import resend
from django.conf import settings


def send_booking_status_email(booking):

    resend.api_key = settings.RESEND_API_KEY

    try:
        response = resend.Emails.send({
            "from": "SK Tours <onboarding@resend.dev>",
            "to": booking.email,
            "subject": f"Booking Status Update - {booking.get_status_display()}",
            "html": f"""
                <h2>Hello {booking.full_name}</h2>

                <p>Your booking status is now:
                <strong>{booking.get_status_display()}</strong></p>

                <h3>Trip Details</h3>

                <ul>
                    <li>Pickup: {booking.pickup_location}</li>
                    <li>Drop: {booking.drop_location}</li>
                    <li>Date & Time: {booking.pickup_datetime}</li>
                    <li>Trip Type: {booking.get_trip_type_display()}</li>
                </ul>

                <p>Thank you for choosing SK Tours & Travels.</p>
            """
        })

        print(response)

        return True, "Email sent successfully."

    except Exception as e:
        print(e)
        return False, str(e)