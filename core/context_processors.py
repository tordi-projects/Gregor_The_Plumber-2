from django.conf import settings


def site_settings(request):
    """Make business details (phone, email, address) available in every template."""
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_PHONE': settings.SITE_PHONE,
        'SITE_EMERGENCY_PHONE': settings.SITE_EMERGENCY_PHONE,
        'SITE_EMAIL': settings.SITE_EMAIL,
        'SITE_ADDRESS': settings.SITE_ADDRESS,
        'SITE_GAS_SAFE_NUMBER': settings.SITE_GAS_SAFE_NUMBER,
    }
