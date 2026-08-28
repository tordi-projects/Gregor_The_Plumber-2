# Luke The Plumber — Django Website

A full Django project for a professional UK (England) plumbing company
website, styled after established UK trade sites (Gas Safe branding,
emergency call-out banners, trust badges, testimonials) with a complete
customer account system (register, log in, log out, profile/dashboard)
and a quote-request booking system.

## Features

- **Public site**: Home, Services (list + detail), About, Contact/quote form
- **Accounts app**: Register, Login, Logout, Profile/dashboard (built on
  Django's built-in auth system, with a custom `Profile` model for phone
  number and address)
- **Quote requests**: Customers (or guests) can submit a job/quote request.
  Logged-in customers can see the status of their own requests on their
  account page (New → Contacted → Quoted → Booked → Completed)
- **Django admin**: Manage services, testimonials and quote requests at
  `/admin/`
- **Responsive, professional UI**: Bootstrap 5 + Bootstrap Icons, custom
  navy/amber theme, sticky mobile "Call Now" button, trust badges (Gas
  Safe Registered, Fully Insured, No Call-Out Fee)

## Project structure

```
luke_the_plumber/
├── manage.py
├── requirements.txt
├── luke_plumber/       # project settings, urls, wsgi/asgi
├── core/                 # public pages, services, testimonials, quote requests
│   ├── models.py         # Service, Testimonial, QuoteRequest
│   ├── management/commands/seed_data.py   # example content loader
│   └── templates/core/
├── accounts/              # registration / login / logout / profile
│   ├── models.py          # Profile (extends the built-in User model)
│   └── templates/accounts/
├── templates/              # base.html (shared layout, navbar, footer)
└── static/                 # css/style.css, js/script.js
```

## Getting started

1. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **(Optional) Load example services and testimonials:**

   ```bash
   python manage.py seed_data
   ```

5. **Create an admin user:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. Visit **http://127.0.0.1:8000/** for the site and
   **http://127.0.0.1:8000/admin/** for the admin panel.

## Key URLs

| Page                     | URL                       |
|---------------------------|---------------------------|
| Home                       | `/`                       |
| Services                   | `/services/`               |
| Service detail              | `/services/<slug>/`         |
| About                       | `/about/`                  |
| Contact / Get a quote        | `/contact/`                |
| Register                    | `/accounts/register/`        |
| Log in                      | `/accounts/login/`           |
| Log out                     | `/accounts/logout/`          |
| My account / dashboard        | `/accounts/profile/`          |
| Django admin                 | `/admin/`                   |

## Admin dashboard + WhatsApp notifications

When a customer submits the contact/quote form:

1. It's saved to the database (visible in Django admin at `/admin/` too).
2. A **WhatsApp message is sent to the business owner** (via Twilio) with
   the customer's name, phone, service, and message.
3. The owner can view and reply to it on a **private staff dashboard** —
   `/staff/` — that only accounts with `is_staff=True` can open. Anyone
   else is redirected to the login page.

On the staff dashboard the owner can:
- See every enquiry, filter by status (New, Contacted, Quoted, Booked,
  Completed, Cancelled)
- Open one to see the full details
- Click a **"Message on WhatsApp"** button (a `wa.me` link) to reply to
  the customer directly on WhatsApp
- Write a reply and update the status — the reply is emailed to the
  customer automatically when saved

### Setting up WhatsApp notifications (Twilio)

1. Create a free account at [twilio.com](https://www.twilio.com).
2. In the Twilio Console, go to **Messaging → Try it out → Send a WhatsApp
   message** to activate the WhatsApp Sandbox. It gives you:
   - A sandbox WhatsApp number (usually `whatsapp:+14155238886`)
   - A join code you send once from **+2347068848255** to that sandbox
     number on WhatsApp (e.g. "join example-word") — this opts your
     number in to receive sandbox messages. This step only applies to
     the free sandbox; a production WhatsApp Business sender doesn't
     need it.
3. Copy your **Account SID** and **Auth Token** from the Twilio Console
   dashboard.
4. Set these environment variables on your host (Render/PythonAnywhere)
   and locally in a `.env`/shell:
   ```
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   ADMIN_WHATSAPP_NUMBER=whatsapp:+2347068848255
   SITE_URL=https://your-deployed-domain.com
   ```
5. Redeploy / restart the app. Submit the contact form to test — you
   should get a WhatsApp message within a few seconds.

**Note:** the Twilio Sandbox is free but only works with numbers that
have joined it, and Twilio may show a sandbox banner on messages. For a
proper production setup (no join step, official green checkmark), apply
for a **WhatsApp Business API sender** through Twilio — it takes Meta a
few days to approve. Nothing else in the code needs to change; you just
swap in the approved sender number for `TWILIO_WHATSAPP_FROM` in step 4.

If Twilio isn't configured yet, the site still works fine — the
notification step is skipped silently (it's logged, not thrown as an
error) so the contact form never breaks because of it.

### Giving someone staff access

Only users with `is_staff=True` can open `/staff/`. To grant this:

```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
u = User.objects.get(username='your-username')
u.is_staff = True
u.save()
```

Or tick the **"Staff status"** checkbox for that user in `/admin/` under
Users (requires a superuser account, created with
`python manage.py createsuperuser`).

## Deploying — fixing "styling was removed"

If the site looks unstyled after deploying, it's almost always because
static files (CSS/JS) aren't being served — `DEBUG=True` serves them
automatically via `runserver`, but production servers need it configured
explicitly. This project already includes [WhiteNoise](https://whitenoise.readthedocs.io/)
for this. Steps below.

### Deploying to Render

1. Push this project to a GitHub repo.
2. In Render, create a **new Web Service** from that repo. Render will
   detect `render.yaml` automatically (or set these manually):
   - **Build command:** `./build.sh`
   - **Start command:** `gunicorn luke_plumber.wsgi:application`
3. Set environment variables in the Render dashboard:
   - `DJANGO_DEBUG` = `False`
   - `DJANGO_SECRET_KEY` = (generate a long random string)
4. Deploy. `build.sh` automatically runs `collectstatic` and `migrate`
   on every deploy, and WhiteNoise serves the collected static files
   directly from Django/Gunicorn — no extra static file configuration
   needed on Render.
5. If you still see unstyled pages, check the deploy logs for a
   `collectstatic` step that actually ran, and hard-refresh your browser
   (Ctrl/Cmd+Shift+R) — browsers cache CSS aggressively.

### Deploying to PythonAnywhere

PythonAnywhere serves static files itself rather than through Django, so
it needs a **static files mapping** set up in the web app config — this
is the step that's usually missed:

1. Upload/clone the project into your PythonAnywhere account (e.g. via
   `git clone` in a Bash console) and install dependencies into a
   virtualenv:
   ```bash
   pip install -r requirements.txt
   ```
2. Run:
   ```bash
   python manage.py collectstatic --no-input
   python manage.py migrate
   ```
   This creates a `staticfiles/` folder with all CSS/JS/icons collected
   in one place.
3. Go to the **Web** tab on PythonAnywhere → **Static files** section,
   and add a mapping:
   - **URL:** `/static/`
   - **Directory:** `/home/yourusername/luke_the_plumber/staticfiles`
   (use your actual username and path)
4. Also set `DJANGO_DEBUG=False` and a real `DJANGO_SECRET_KEY` as
   environment variables in the **Web** tab (or in your WSGI file).
5. Click **Reload** on the Web tab.

WhiteNoise is also included as a fallback, so even if you skip step 3
the CSS/JS should still load — but the PythonAnywhere static mapping in
step 3 is faster and is the recommended approach for that platform.

### Common causes if styling is still missing after the above

- `collectstatic` was never run (no `staticfiles/` folder exists yet).
- `DEBUG=True` was left on with a platform that doesn't auto-serve
  static files the way `runserver` does.
- Browser cache — try an incognito/private window.
- The static mapping directory on PythonAnywhere points to the wrong
  path (double-check the username and folder name).

## Before deploying to production

- Set `DJANGO_DEBUG=False` and a real `DJANGO_SECRET_KEY` as environment
  variables.
- Set `DJANGO_ALLOWED_HOSTS` to your real domain(s).
- Swap `EMAIL_BACKEND` in `settings.py` for a real SMTP provider so quote
  request notifications can be emailed out.
- Swap SQLite for PostgreSQL (or similar) for production use.
- Update the business details in `settings.py` (`SITE_PHONE`,
  `SITE_EMAIL`, `SITE_ADDRESS`, `SITE_GAS_SAFE_NUMBER`, etc.) with the
  real company details, including the real Gas Safe registration number.
- Run `python manage.py collectstatic`.

## Customising content

- **Services & testimonials**: edit via `/admin/`, or edit the example
  data in `core/management/commands/seed_data.py` and re-run
  `python manage.py seed_data`.
- **Business details** (phone numbers, email, address, Gas Safe number):
  edit the constants at the bottom of `luke_plumber/settings.py` — they
  automatically appear across the whole site via
  `core/context_processors.py`.
- **Colours / branding**: edit the CSS variables at the top of
  `static/css/style.css` (`--navy-900`, `--amber-500`, etc.).
