"""
Sends a WhatsApp alert to the business owner whenever a new quote request
comes in, using Twilio's WhatsApp API.

This is written to fail *safely*: if Twilio isn't configured yet (no
account SID/auth token in the environment), the contact form still works
and the request is still saved — it just skips the WhatsApp step and logs
a warning instead of crashing the page.
"""

import logging

from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)


def send_whatsapp_notification(quote_request):
    """Send a WhatsApp message to the admin about a new QuoteRequest.

    Returns True if the message was sent successfully, False otherwise.
    """
    account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
    auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
    from_number = getattr(settings, 'TWILIO_WHATSAPP_FROM', '')
    to_number = getattr(settings, 'ADMIN_WHATSAPP_NUMBER', '')

    if not all([account_sid, auth_token, from_number, to_number]):
        logger.warning(
            "WhatsApp notification skipped for quote request #%s — "
            "Twilio isn't configured (set TWILIO_ACCOUNT_SID and "
            "TWILIO_AUTH_TOKEN as environment variables).",
            quote_request.pk,
        )
        return False

    try:
        from twilio.rest import Client
    except ImportError:
        logger.error(
            "WhatsApp notification skipped — the 'twilio' package isn't "
            "installed. Run: pip install twilio"
        )
        return False

    dashboard_link = ''
    try:
        path = reverse('core:staff_quote_detail', args=[quote_request.pk])
        dashboard_link = f"{settings.SITE_URL}{path}"
    except Exception:
        pass

    emergency_flag = "\n*EMERGENCY JOB*" if quote_request.is_emergency else ""
    service_name = quote_request.service.name if quote_request.service else "General enquiry"

    body = (
        f"*New job request — Luke The Plumber*{emergency_flag}\n\n"
        f"Name: {quote_request.full_name}\n"
        f"Phone: {quote_request.phone}\n"
        f"Service: {service_name}\n"
        f"Address: {quote_request.address}\n\n"
        f"Message:\n{quote_request.message}\n"
    )
    if dashboard_link:
        body += f"\nView & reply: {dashboard_link}"

    try:
        client = Client(account_sid, auth_token)
        client.messages.create(body=body, from_=from_number, to=to_number)
        quote_request.whatsapp_notified = True
        quote_request.save(update_fields=['whatsapp_notified'])
        return True
    except Exception as exc:  # noqa: BLE001 — log and continue, never break the form
        logger.error("Failed to send WhatsApp notification for quote request #%s: %s",
                     quote_request.pk, exc)
        return False
