from django.core.management.base import BaseCommand
from core.models import Service, Testimonial


SERVICES = [
    dict(
        name='Emergency Plumbing', icon='bi-exclamation-triangle-fill',
        short_description='Burst pipes, leaks and floods — fast response, day or night.',
        description=(
            "Water doesn't wait for office hours, and neither do we. Our emergency "
            "plumbers are on call 24 hours a day, 7 days a week across London and "
            "the surrounding counties. Whether it's a burst pipe, a serious leak or "
            "a flooded kitchen, we aim to be with you within the hour to stop the "
            "damage and get things back under control."
        ),
        price_from=79, is_emergency=True, order=1,
    ),
    dict(
        name='Boiler Repair & Installation', icon='bi-fire',
        short_description='Gas Safe registered engineers for boiler servicing, repairs and new installs.',
        description=(
            "From an annual service to a full replacement, our Gas Safe registered "
            "engineers work on all major boiler brands including Worcester Bosch, "
            "Vaillant, Baxi and Ideal. We'll always give you a clear, upfront price "
            "before any work begins, and every installation comes with a full "
            "manufacturer's warranty."
        ),
        price_from=90, is_emergency=True, order=2,
    ),
    dict(
        name='Bathroom Installation', icon='bi-water',
        short_description='Full bathroom fit-outs, from a simple refit to a complete redesign.',
        description=(
            "We design and install bathrooms and en-suites from start to finish, "
            "handling everything from first fix pipework to tiling, fitting and "
            "final snagging. We'll work with your own suite and tiles or help you "
            "choose from trusted suppliers."
        ),
        price_from=1250, is_emergency=False, order=3,
    ),
    dict(
        name='Leak Detection', icon='bi-droplet-fill',
        short_description='Non-invasive leak detection to find hidden leaks without unnecessary damage.',
        description=(
            "Using thermal imaging and acoustic detection equipment, we can pinpoint "
            "hidden leaks behind walls, under floors and underground without "
            "tearing your property apart, saving you time and repair costs."
        ),
        price_from=95, is_emergency=False, order=4,
    ),
    dict(
        name='Drain Unblocking', icon='bi-arrow-down-circle-fill',
        short_description='CCTV drain surveys and high-pressure jetting to clear stubborn blockages.',
        description=(
            "Slow-draining sinks, gurgling toilets or a blocked outside drain — our "
            "team uses CCTV drain cameras and high-pressure jetting to clear "
            "blockages quickly and diagnose any underlying issues with the drain run."
        ),
        price_from=85, is_emergency=True, order=5,
    ),
    dict(
        name='Central Heating & Powerflushing', icon='bi-thermometer-half',
        short_description='System upgrades, radiator installs and powerflushing for even, efficient heat.',
        description=(
            "Cold spots on your radiators or a system that's on its last legs? We "
            "install and upgrade central heating systems and offer powerflushing to "
            "remove sludge and debris, improving efficiency and extending the life "
            "of your boiler."
        ),
        price_from=180, is_emergency=False, order=6,
    ),
    dict(
        name='Water Tanks & Cylinders', icon='bi-cup-hot-fill',
        short_description='Supply, repair and replacement of cold water tanks and hot water cylinders.',
        description=(
            "We supply, repair and replace cold water storage tanks and unvented "
            "and vented hot water cylinders, helping you get reliable hot water "
            "pressure throughout your home."
        ),
        price_from=350, is_emergency=False, order=7,
    ),
    dict(
        name='General Plumbing & Repairs', icon='bi-tools',
        short_description='Taps, toilets, washing machines and everyday plumbing jobs, done properly.',
        description=(
            "From a dripping tap to fitting a new washing machine or dishwasher, our "
            "friendly local plumbers handle the everyday jobs with the same care "
            "and attention as the big ones."
        ),
        price_from=65, is_emergency=False, order=8,
    ),
]

TESTIMONIALS = [
    dict(
        customer_name='Sarah M.', location='Clapham, London', rating=5,
        comment=(
            "Called Luke The Plumber on a Sunday morning after a pipe burst under "
            "the kitchen sink. An engineer was at the door within 40 minutes and "
            "had it fixed before lunch. Brilliant service and very reasonably priced."
        ),
    ),
    dict(
        customer_name='David O.', location='Richmond, London', rating=5,
        comment=(
            "Had a full bathroom refit done and couldn't be happier. Tidy, punctual "
            "and the finish is excellent. They talked us through every step and "
            "stuck to the quote they gave us."
        ),
    ),
    dict(
        customer_name='Priya K.', location='St Albans, Hertfordshire', rating=5,
        comment=(
            "Our boiler packed in during a cold snap. The engineer diagnosed the "
            "fault quickly, had the part on the van, and we had heating again the "
            "same afternoon. Highly recommend."
        ),
    ),
    dict(
        customer_name='Tom H.', location='Guildford, Surrey', rating=4,
        comment=(
            "Good, honest plumbing work at a fair price. They found a hidden leak "
            "under the drive that two other companies had missed."
        ),
    ),
]


class Command(BaseCommand):
    help = "Seed the database with example services and testimonials for Luke The Plumber."

    def handle(self, *args, **options):
        created_services = 0
        for data in SERVICES:
            _, created = Service.objects.get_or_create(name=data['name'], defaults=data)
            created_services += int(created)

        created_testimonials = 0
        for data in TESTIMONIALS:
            _, created = Testimonial.objects.get_or_create(
                customer_name=data['customer_name'], defaults=data
            )
            created_testimonials += int(created)

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete: {created_services} services and "
            f"{created_testimonials} testimonials created."
        ))
