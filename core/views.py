from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import QuoteRequestForm, AdminReplyForm
from .models import Service, Testimonial, QuoteRequest
from .services import send_whatsapp_notification


def home(request):
    services = Service.objects.all()[:6]
    testimonials = Testimonial.objects.filter(is_featured=True)[:3]
    context = {
        'services': services,
        'testimonials': testimonials,
    }
    return render(request, 'core/home.html', context)


def about(request):
    testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    return render(request, 'core/about.html', {'testimonials': testimonials})


def service_list(request):
    services = Service.objects.all()
    return render(request, 'core/services.html', {'services': services})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    other_services = Service.objects.exclude(pk=service.pk)[:3]
    return render(request, 'core/service_detail.html', {
        'service': service,
        'other_services': other_services,
    })


def contact(request):
    initial = {}
    if request.user.is_authenticated:
        initial = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'phone': getattr(getattr(request.user, 'profile', None), 'phone_number', ''),
        }

    preselected_service = request.GET.get('service')
    if preselected_service:
        initial['service'] = Service.objects.filter(slug=preselected_service).first()

    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote_request = form.save(commit=False)
            if request.user.is_authenticated:
                quote_request.user = request.user
            quote_request.save()
            send_whatsapp_notification(quote_request)
            messages.success(
                request,
                "Thanks — your request has been received. A member of the Luke The "
                "Plumber team will be in touch shortly."
            )
            return redirect('core:contact')
    else:
        form = QuoteRequestForm(initial=initial)

    return render(request, 'core/contact.html', {'form': form})


# -------------------------------------------------------------------
# Private staff dashboard — only accounts with is_staff=True can access
# these pages. Anyone else is redirected to the login page.
# -------------------------------------------------------------------

@staff_member_required(login_url='accounts:login')
def staff_dashboard(request):
    status_filter = request.GET.get('status', '')
    quote_requests = QuoteRequest.objects.select_related('service', 'user').all()
    if status_filter:
        quote_requests = quote_requests.filter(status=status_filter)

    context = {
        'quote_requests': quote_requests,
        'status_filter': status_filter,
        'status_choices': QuoteRequest.Status.choices,
        'new_count': QuoteRequest.objects.filter(status=QuoteRequest.Status.NEW).count(),
        'emergency_count': QuoteRequest.objects.filter(
            is_emergency=True, status=QuoteRequest.Status.NEW
        ).count(),
    }
    return render(request, 'core/staff_dashboard.html', context)


@staff_member_required(login_url='accounts:login')
def staff_quote_detail(request, pk):
    quote_request = get_object_or_404(QuoteRequest, pk=pk)

    if request.method == 'POST':
        form = AdminReplyForm(request.POST, instance=quote_request)
        if form.is_valid():
            reply_text = form.cleaned_data.get('admin_reply', '').strip()
            updated = form.save(commit=False)

            if reply_text:
                updated.replied_at = timezone.now()
                try:
                    send_mail(
                        subject=f"Re: your enquiry with {settings.SITE_NAME}",
                        message=(
                            f"Hi {quote_request.full_name},\n\n{reply_text}\n\n"
                            f"— {settings.SITE_NAME}\n{settings.SITE_PHONE}"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[quote_request.email],
                        fail_silently=True,
                    )
                    messages.success(request, "Reply saved and emailed to the customer.")
                except Exception:
                    messages.warning(request, "Reply saved, but the email couldn't be sent.")
            else:
                messages.success(request, "Status updated.")

            updated.save()
            return redirect('core:staff_quote_detail', pk=pk)
    else:
        form = AdminReplyForm(instance=quote_request)

    return render(request, 'core/staff_quote_detail.html', {
        'quote_request': quote_request,
        'form': form,
    })
