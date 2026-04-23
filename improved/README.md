# 🏏 CRICIFY — Cricket Hub Website

A modern Django-based cricket information website.

## Features
- 🔴 Live match scores & tracking
- 📅 Upcoming & completed matches
- 📰 Cricket news with detail pages
- 🏆 Team profiles with full squad
- 👤 Player profiles with stats
- 📊 Points table with NRR
- 🔍 Search across all content
- 🌙 Dark / Light theme toggle
- 📱 Fully responsive design

## Setup

```bash
# Install dependencies
pip install django pillow

# Run migrations
python manage.py migrate

# Create superuser (for admin)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run server
python manage.py runserver
```

## Environment Variables (for production)
```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Project Structure
```
cricify/
├── core/              ← Main app
│   ├── models.py      ← Team, Player, Match, News, PointsTable
│   ├── views.py       ← All page views + search
│   ├── urls.py        ← URL routes
│   └── admin.py       ← Admin panel config
├── templates/
│   ├── base.html      ← Layout with navbar & footer
│   └── core/          ← 10 page templates
├── static/
│   ├── css/style.css  ← Full responsive CSS with dark/light
│   └── js/theme.js    ← Theme toggle + mobile menu
└── manage.py
```

## URLs
| URL | Page |
|-----|------|
| / | Home (live matches, news, points) |
| /matches/ | All matches |
| /matches/<id>/ | Match detail |
| /news/ | All news |
| /news/<slug>/ | News article detail |
| /teams/ | All teams |
| /teams/<id>/ | Team detail + squad |
| /players/ | Players (filterable by role/team) |
| /players/<id>/ | Player profile |
| /points-table/ | Full standings |
| /search/?q=query | Search results |
| /admin/ | Django admin |
