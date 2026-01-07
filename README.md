# Coderr Backend

This is the backend for **Coderr**, a platform for managing offers, orders, profiles, and reviews.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Technologies](#technologies)
- [License](#license)

---

## Features

- User registration, login, and account management
- Create, update, and manage Offers
- Place and manage Orders
- User Profiles with editable details
- Add and view Reviews for offers/orders
- REST API ready for frontend or external integrations

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/BedirhanMehmetSoylu/Coderr-Backend
cd Coderr-Backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/registration/` – Register a new user
- `POST /api/login/` – Login user

### Profile
- `GET /api/profile/{pk}/` – Retrieve profile details
- `PATCH /api/profile/{pk}/` – Update profile
- `GET /api/profiles/business/` – List all business profiles
- `GET /api/profiles/customer/` – List all customer profiles

### Offers
- `GET /api/offers/` – List all offers
- `POST /api/offers/` – Create a new offer
- `GET /api/offers/{id}/` – Retrieve offer details
- `PATCH /api/offers/{id}/` – Update an offer
- `DELETE /api/offers/{id}/` – Delete an offer
- `GET /api/offerdetails/{id}/` – Retrieve detailed offer info

### Orders
- `GET /api/orders/` – List all orders
- `POST /api/orders/` – Create a new order
- `PATCH /api/orders/{id}/` – Update an order
- `DELETE /api/orders/{id}/` – Delete an order
- `GET /api/order-count/{business_user_id}/` – Get total orders for a business user
- `GET /api/completed-order-count/{business_user_id}/` – Get completed orders for a business user

### Reviews
- `GET /api/reviews/` – List all reviews
- `POST /api/reviews/` – Add a review
- `PATCH /api/reviews/{id}/` – Update a review
- `DELETE /api/reviews/{id}/` – Delete a review

### Aggregated / Cross‑Domain Endpoints
- `GET /api/base-info/` – Retrieve aggregated platform information (overview, stats, etc.)

## Authentication

- Uses Django REST Framework authentication

- Supports token-based authentication via Simple JWT

- Most endpoints require authenticated users

## Technologies

- Python 3.13.5

- Django 6.0

- Django REST Framework

- PostgreSQL / SQLite (depending on environment)

- DRF Token Authentication

## License
This project is licensed under the MIT License.
