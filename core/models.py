from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Service(models.Model):
    """A plumbing / heating service offered by the company."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        default='bi-wrench',
        help_text="Bootstrap Icons class, e.g. 'bi-droplet-fill', 'bi-fire', 'bi-wrench'."
    )
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    price_from = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="Optional 'prices from' figure shown on the service card."
    )
    is_emergency = models.BooleanField(
        default=False, help_text="Show this service on the 24/7 emergency callout section."
    )
    order = models.PositiveIntegerField(default=0, help_text="Controls display order (lowest first).")

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:service_detail', kwargs={'slug': self.slug})


class Testimonial(models.Model):
    """A customer review, shown on the homepage and about page."""

    customer_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, help_text="e.g. 'Clapham, London'")
    rating = models.PositiveSmallIntegerField(
        default=5,
        choices=[(i, f"{i} star{'s' if i != 1 else ''}") for i in range(1, 6)]
    )
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} ({self.rating}★)"


class QuoteRequest(models.Model):
    """A job / quote request submitted through the contact form."""

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        CONTACTED = 'contacted', 'Contacted'
        QUOTED = 'quoted', 'Quoted'
        BOOKED = 'booked', 'Booked'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='quote_requests'
    )
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='quote_requests'
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, help_text="Property address, including postcode.")
    is_emergency = models.BooleanField(default=False, help_text="Tick if this is an urgent/emergency job.")
    message = models.TextField(help_text="Describe the job / issue.")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    # Admin-only fields — the private reply the business owner writes back
    # to the customer from the staff dashboard.
    admin_reply = models.TextField(blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    whatsapp_notified = models.BooleanField(
        default=False, help_text="Whether the WhatsApp alert to the admin was sent successfully."
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Quote request from {self.full_name} ({self.created_at:%d %b %Y})"

    @property
    def whatsapp_reply_url(self):
        """A wa.me link the admin can click to message this customer directly on WhatsApp."""
        digits = ''.join(ch for ch in self.phone if ch.isdigit())
        if not digits:
            return ''
        # Assume UK numbers if no country code was given (starts with 0).
        if digits.startswith('0'):
            digits = '44' + digits[1:]
        return f"https://wa.me/{digits}"
