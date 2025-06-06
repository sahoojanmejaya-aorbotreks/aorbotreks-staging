# Aorbo Treks Website

A Django-based website for Aorbo Treks, a platform connecting trekkers with local trek organizers.

## Project Overview

This website was converted from a static HTML/CSS/JS website to a Django-based web application. The frontend design has been preserved while the backend has been migrated to Django.

## Features

- Responsive design
- Contact form with database storage
- Admin interface for managing contacts
- Multiple pages including Home, About, Blogs, Safety, and Contact

## Tech Stack

- Django 5.0.1
- MySQL
- HTML/CSS/JavaScript
- Bootstrap

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd aorbo_website
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Create a MySQL database named `aorbo_contacts`
   - Update the database credentials in `aorbo_project/settings.py` if needed

4. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser for the admin interface:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the website at `http://127.0.0.1:8000/`

## Project Structure

- `aorbo_project/`: Django project settings
- `treks_app/`: Main Django application
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, images)
- `media/`: User-uploaded files

## Admin Interface

Access the admin interface at `http://127.0.0.1:8000/admin/` using the superuser credentials you created.

## Contact

For any inquiries, please contact:
- Email: info@aorbotreks.com
- Phone: +91 939 809 3503
