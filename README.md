# Prime Cuts Salon & Barbershop -- Booking Website

A Django website for a hair salon/barbershop with online appointment scheduling.

## Quick start

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Demo accounts (already seeded in db.sqlite3)

| Role    | Username      | Password           |
|---------|---------------|---------------------|
| Admin   | admin         | AdminPass123!        |
| Stylist | jide.stylist  | StylistPass123!      |
| Stylist | ada.stylist   | StylistPass123!      |
| Client  | client1       | ClientPass123!        |

If you migrate on a fresh (empty) database, register a new client account from
the site, and create stylist/admin accounts from `/admin/`.

## Apps

- **accounts** -- custom User model with `role` (client / stylist / admin)
- **services** -- catalogue of salon services offered (haircuts, coloring, braiding, etc.)
- **appointments** -- Availability (a stylist's weekly free hours) and
  Appointment (a booking) models, plus the booking views and dashboards
- **core** -- home, about, contact pages

## Sample data seeded

- Services: Men's Haircut, Beard Trim & Shape-Up, Hair Coloring, Braiding, Kids' Haircut
- Stylists: Jide Okafor (Fades & Classic Cuts), Ada Nwosu (Braiding & Natural Hair)

## Deploying this project

This project is pre-configured for deployment to Vercel (external Postgres
database, environment-variable driven settings, `vercel.json`,
`requirements.txt`). See the accompanying deployment guide for full,
step-by-step instructions covering: extracting this zip, opening it in
VS Code, pushing it to GitHub, and deploying it live on Vercel with a free
Postgres database.
