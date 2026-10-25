# Vehicle Inventory & Booking REST API

## 1. Project Overview

This project is a REST API built using Django REST Framework to manage vehicles and customer bookings.

## 2. Technologies Used

- Python
- Django
- Django REST Framework
- SQLite

## 3. Installation

Create and activate a virtual environment:

```bash
python -m venv env
env\Scripts\activate
```

Install dependencies:

```bash
pip install django djangorestframework django-filter python-dotenv
```

## 4. Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Run the Project

```bash
python manage.py runserver
```

The local API base URL is:

`http://127.0.0.1:8000/api/`

## 6. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/vehicles/` | List vehicles |
| POST | `/api/vehicles/` | Create a vehicle |
| GET | `/api/vehicles/<id>/` | Retrieve a vehicle |
| PUT | `/api/vehicles/<id>/` | Update a vehicle |
| DELETE | `/api/vehicles/<id>/` | Delete a vehicle |
| GET | `/api/bookings/` | List bookings |
| POST | `/api/bookings/` | Create a booking |
| GET | `/api/bookings/<id>/` | Retrieve a booking |

## 7. Vehicle Filters

- `/api/vehicles/?brand=Toyota`
- `/api/vehicles/?fuel_type=Diesel`
- `/api/vehicles/?is_available=true`

## 8. Sample Booking Request

POST `/api/bookings/`

```json
{
  "vehicle": 1,
  "customer_name": "Anu",
  "customer_phone": "9876543210",
  "start_date": "2026-11-01",
  "end_date": "2026-11-04"
}
```

The total amount is calculated automatically from the booking duration and vehicle's daily price.

## 9. Booking Validations

- Phone number must contain exactly 10 digits.
- Start date cannot be in the past.
- End date must be after the start date.
- Overlapping bookings are rejected.
- A booked vehicle is marked unavailable.

## 10. Test the Project

Run the development server and test the endpoints using the Django REST Framework browsable API or Postman.

Run the Django system check:

```bash
python manage.py check
```

## 11. Screen Recording

Recording link: https://drive.google.com/file/d/1mhi_dDJTT8ma_xYlC8QHvldQkxqmpi_e/view?usp=drive_link
## 12. Live Deployment

Live API URL: 

