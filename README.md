# E-Commerce Platform Backend

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-green?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-red?logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

This repository contains a Django-based e-commerce backend that provides a robust RESTful API for an online marketplace. Built with Django REST Framework (DRF), it supports full e-commerce functionality including user authentication, product catalog management, shopping cart, orders processing, payments, and reviews. The backend is designed with a multi-vendor architecture, allowing users to operate as sellers with their own stores. It also integrates Celery for background tasks (such as sending order notifications) and uses Redis for caching and as a message broker. The application is fully containerized with Docker and ready for deployment with Gunicorn and Nginx.

## Features

- User Authentication & Accounts: User registration, JWT-based login (using Simple JWT), and profile management (including updating profile info and managing shipping addresses).
- Multi-Vendor Stores: Users can register as sellers to create and manage their own stores. Sellers can add products to their store inventory, set prices (including discounts), and manage stock.
- Product Catalog & Categories: Create, update, and list products with support for categories (hierarchical categories for product organization). The API provides product listings, detail views, and search/filtering capabilities (e.g. by category, price, or name).
- Shopping Cart: Customers can add products (store items) to a cart, update item quantities, and remove items. The cart API calculates total price and supports discounts on items.
- Order Management: Customers can place orders from their cart, providing address information for delivery. The system tracks order status (e.g., Pending, Processing, Delivered, Canceled) and order history. Sellers can view orders for their products (seller dashboard) and update order statuses.
- Payment Processing: Integration for recording payments of orders (e.g., capturing payment amount, transaction ID, status, and timestamp). This can be extended to integrate with payment gateways. Orders can be marked as paid upon successful transaction.
- Reviews & Ratings: Customers can leave reviews/ratings for products they have purchased, helping to provide feedback and ratings in the product catalog.
- Asynchronous Notifications: Uses Celery with Redis to handle background tasks. For example, sending order confirmation emails or status update notifications to customers is handled asynchronously.
- Admin Panel: Customized Django Admin interfaces for managing users, products, orders, etc., with search and filter capabilities. This is useful for internal administration of the platform.
- Soft Deletes: Instead of hard-deleting records, the models implement logical deletion (via an is_active flag in a base model) to preserve data integrity. Inactive records are filtered out from regular queries by default.
- API Documentation: Interactive API docs are provided via Swagger UI (and ReDoc) for quick testing and exploration of the available endpoints.

## Technology Stack

- Language & Framework: Python 3.x, Django (backend web framework), Django REST Framework (API development).
- Authentication: JWT authentication using djangorestframework-simplejwt (securely handle login and token refresh, with token blacklist support).
- Database: PostgreSQL used as the primary relational database for storing all persistent data.
- Caching & Messaging: Redis used for caching (via django-redis) and as a message broker for Celery tasks.
- Asynchronous Tasks: Celery for background job processing (such as sending emails or other long-running tasks), configured with Redis as broker/result backend.
- API Documentation: drf-yasg integrated to generate Swagger UI and ReDoc documentation for the API.
- Containerization: Docker and Docker Compose used to containerize the application (including separate services for Django, PostgreSQL, Redis, Celery, etc.). Gunicorn is used as the WSGI server in the container, with Nginx as a reverse proxy and static file server for production deployment.
- Others: python-decouple for configuration via .env files, django-cors-headers for handling Cross-Origin Resource Sharing (CORS), django-filter for enabling query parameter filtering in APIs.

## Project Structure

`bash
backend/
├── core/                     # Django project settings and configuration
│   ├── settings.py           # Django settings (configured with env variables)
│   ├── urls.py               # URL routes, including API and documentation routes
│   ├── wsgi.py               # WSGI application (for Gunicorn)
│   ├── asgi.py               # ASGI application (for future scope, e.g., async support)
│   ├── celery.py             # Celery application configuration
│   └── init.py
├── accounts/                 # User accounts app (custom User model, auth)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ... (admin, tests, etc.)
├── base/                     # Base app (abstract models, base admin classes, common utilities)
│   ├── models.py             # BaseModel (includes is_active for soft delete)
│   ├── admin.py              # BaseAdmin (includes common admin configurations)
│   └── ...
├── products/                 # Products app (Product, Category, ProductImage models)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── stores/                   # Stores app (Store and StoreItem models, linking Products to Sellers)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── carts/                    # Carts app (shopping cart and cart items)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── orders/                   # Orders app (orders and order items)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py              # Celery tasks (e.g., sending emails on order status change)
│   ├── urls.py
│   └── ...
├── payments/                 # Payments app (payment records for orders)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── reviews/                  # Reviews app (product reviews and ratings)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── locations/                # Locations app (addresses for users)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── docs/
│   └── E-CommercePlatformERD.png   # Entity-Relationship Diagram for the project
├── manage.py                 # Django manage.py for command-line executions
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker image configuration for the Django app
├── docker-compose.yml        # Docker Compose definitions for all services (web, db, redis, etc.)
└── README.md

Hamed, [8/15/25 1:23 PM]
# E-Commerce Platform Backend

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-green?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-red?logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

This repository contains a Django-based e-commerce backend that provides a robust RESTful API for an online marketplace. Built with Django REST Framework (DRF), it supports full e-commerce functionality including user authentication, product catalog management, shopping cart, orders processing, payments, and reviews. The backend is designed with a multi-vendor architecture, allowing users to operate as sellers with their own stores. It also integrates Celery for background tasks (such as sending order notifications) and uses Redis for caching and as a message broker. The application is fully containerized with Docker and ready for deployment with Gunicorn and Nginx.

## Features

- User Authentication & Accounts: User registration, JWT-based login (using Simple JWT), and profile management (including updating profile info and managing shipping addresses).
- Multi-Vendor Stores: Users can register as sellers to create and manage their own stores. Sellers can add products to their store inventory, set prices (including discounts), and manage stock.
- Product Catalog & Categories: Create, update, and list products with support for categories (hierarchical categories for product organization). The API provides product listings, detail views, and search/filtering capabilities (e.g. by category, price, or name).
- Shopping Cart: Customers can add products (store items) to a cart, update item quantities, and remove items. The cart API calculates total price and supports discounts on items.
- Order Management: Customers can place orders from their cart, providing address information for delivery. The system tracks order status (e.g., Pending, Processing, Delivered, Canceled) and order history. Sellers can view orders for their products (seller dashboard) and update order statuses.
- Payment Processing: Integration for recording payments of orders (e.g., capturing payment amount, transaction ID, status, and timestamp). This can be extended to integrate with payment gateways. Orders can be marked as paid upon successful transaction.
- Reviews & Ratings: Customers can leave reviews/ratings for products they have purchased, helping to provide feedback and ratings in the product catalog.
- Asynchronous Notifications: Uses Celery with Redis to handle background tasks. For example, sending order confirmation emails or status update notifications to customers is handled asynchronously.
- Admin Panel: Customized Django Admin interfaces for managing users, products, orders, etc., with search and filter capabilities. This is useful for internal administration of the platform.
- Soft Deletes: Instead of hard-deleting records, the models implement logical deletion (via an is_active flag in a base model) to preserve data integrity. Inactive records are filtered out from regular queries by default.
- API Documentation: Interactive API docs are provided via Swagger UI (and ReDoc) for quick testing and exploration of the available endpoints.

## Technology Stack

- Language & Framework: Python 3.x, Django (backend web framework), Django REST Framework (API development).
- Authentication: JWT authentication using djangorestframework-simplejwt (securely handle login and token refresh, with token blacklist support).
- Database: PostgreSQL used as the primary relational database for storing all persistent data.

Hamed, [8/15/25 1:23 PM]
- Caching & Messaging: Redis used for caching (via django-redis) and as a message broker for Celery tasks.
- Asynchronous Tasks: Celery for background job processing (such as sending emails or other long-running tasks), configured with Redis as broker/result backend.
- API Documentation: drf-yasg integrated to generate Swagger UI and ReDoc documentation for the API.
- Containerization: Docker and Docker Compose used to containerize the application (including separate services for Django, PostgreSQL, Redis, Celery, etc.). Gunicorn is used as the WSGI server in the container, with Nginx as a reverse proxy and static file server for production deployment.
- Others: python-decouple for configuration via .env files, django-cors-headers for handling Cross-Origin Resource Sharing (CORS), django-filter for enabling query parameter filtering in APIs.

## Project Structure

`bash
backend/
├── core/                     # Django project settings and configuration
│   ├── settings.py           # Django settings (configured with env variables)
│   ├── urls.py               # URL routes, including API and documentation routes
│   ├── wsgi.py               # WSGI application (for Gunicorn)
│   ├── asgi.py               # ASGI application (for future scope, e.g., async support)
│   ├── celery.py             # Celery application configuration
│   └── init.py
├── accounts/                 # User accounts app (custom User model, auth)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ... (admin, tests, etc.)
├── base/                     # Base app (abstract models, base admin classes, common utilities)
│   ├── models.py             # BaseModel (includes is_active for soft delete)
│   ├── admin.py              # BaseAdmin (includes common admin configurations)
│   └── ...
├── products/                 # Products app (Product, Category, ProductImage models)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── stores/                   # Stores app (Store and StoreItem models, linking Products to Sellers)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── carts/                    # Carts app (shopping cart and cart items)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── orders/                   # Orders app (orders and order items)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py              # Celery tasks (e.g., sending emails on order status change)
│   ├── urls.py
│   └── ...
├── payments/                 # Payments app (payment records for orders)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── reviews/                  # Reviews app (product reviews and ratings)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── locations/                # Locations app (addresses for users)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── docs/
│   └── E-CommercePlatformERD.png   # Entity-Relationship Diagram for the project
├── manage.py                 # Django manage.py for command-line executions
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker image configuration for the Django app
├── docker-compose.yml        # Docker Compose definitions for all services (web, db, redis, etc.)
└── README.md


<details>
  <summary><strong>Entity Relationship Diagram</strong></summary>
  <br/>
  ![ERD Diagram](backend/docs/E-CommercePlatformERD.png)
</details>

Environment Configuration

The application uses python-decouple to manage configuration through environment variables. You should create a .env file in the project root (or provide these in your Docker Compose configuration) with the following keys:

SECRET_KEY: Django secret key for cryptographic signing.

DEBUG: Debug mode flag (True for development, False for production).

DB_NAME: PostgreSQL database name.

DB_USER: PostgreSQL database username.

DB_PASSWORD: PostgreSQL database user password.

DB_HOST: Database host (e.g., localhost or the database service name in Docker Compose).

DB_PORT: Database port (default PostgreSQL is 5432).

REDIS_LOCATION: Redis connection URI for caching (e.g., redis://localhost:6379/0 or Docker service name).

CELERY_BROKER_REDIS_URL: Redis connection URI for Celery broker (e.g., redis://localhost:6379/1).

CELERY_RESULT_BACKEND: Redis connection URI for Celery result backend (can be the same Redis instance).

EMAIL_HOST: SMTP server host for sending emails (if using email features, e.g., Gmail SMTP).

EMAIL_PORT: SMTP server port.

EMAIL_HOST_USER: SMTP username.

EMAIL_HOST_PASSWORD: SMTP password.

EMAIL_USE_TLS: True/False whether to use TLS for email.

EMAIL_USE_SSL: True/False whether to use SSL for email.


Make sure to set the database and email values according to your own environment. If running via Docker, these will typically be set in the docker-compose.yml file under the service environment.

Getting Started

Below are instructions to set up and run the project for development and testing purposes.

Running with Docker

Ensure you have Docker and Docker Compose installed. The provided docker-compose.yml sets up multiple services (Django app, PostgreSQL, Redis, and possibly Celery workers). Use the following steps:

1. Build and start the containers (in the background):

docker-compose up -d --build

This will build the Docker image for the Django app and start all services (database, redis, web, etc.) as defined in the compose file.


2. Apply database migrations to set up the PostgreSQL database schema:

docker-compose exec web python manage.py migrate

(The service name web may vary if different in the Compose file, adjust accordingly.)


3. Create a superuser account for accessing the Django admin:

docker-compose exec web python manage.py createsuperuser

Follow the prompts to set up an admin username, email, and password.


4. Collect static files (for production deployment):

docker-compose exec web python manage.py collectstatic --no-input

This will gather all static files to the static directory (which Nginx can serve in production).


5. Access the application:

The API is served at http://localhost/api/ (e.g., you can visit http://localhost/api/products/ to see the products API).

The Swagger UI documentation is available at http://localhost/swagger/ for interactive API browsing.

The Django Admin Panel can be accessed at http://localhost/admin/ (use the superuser credentials created earlier).

(If the Docker setup includes Nginx, the default port might be 80; otherwise it could be 8000. Adjust the URL accordingly, e.g., http://localhost:8000/ if needed.)


Note: Docker Compose will also likely start the Celery worker and beat services if they are defined in the compose file. Check the compose configuration to confirm service names (often something like celeryworker and celerybeat). If they are not automatically started, you can run them as needed (see Celery section below).



Running Locally (Without Docker)

If you prefer to run the project on your local machine without Docker, follow these steps:

1. Clone the repository and navigate into the project directory.


2. Create a virtual environment using Python 3 and activate it:

python3 -m venv venv
source venv/bin/activate

(On Windows, use venv\Scripts\activate.)


3. Install dependencies from the requirements.txt file:

pip install -r requirements.txt


4. Setup the database: Ensure you have PostgreSQL running and create a database matching DB_NAME in your .env. Also, have Redis running if you want to use Celery and caching. Update the .env with your database and Redis connection details.


5. Apply migrations to create database tables:

python manage.py migrate


6. Create a superuser for admin access:

python manage.py createsuperuser


7. Run the development server:

python manage.py runserver

By default, this will serve the application at http://127.0.0.1:8000/.


8. Access the application as with Docker:

API endpoints under http://127.0.0.1:8000/api/

Swagger UI at http://127.0.0.1:8000/swagger/

Admin at http://127.0.0.1:8000/admin/




Running Celery Workers (Background Tasks)

To process background tasks like sending emails, you need to run Celery. If using Docker and the compose file includes Celery, the workers might already be running as separate services. If not, or if running locally, follow these steps:

Start the Celery worker to handle asynchronous tasks:

celery -A core worker --loglevel=info

This assumes your current directory is the Django project root (where core is the Django project name).

Start the Celery beat scheduler (if you have scheduled tasks, e.g., using django-celery-beat for periodic tasks):

celery -A core beat --loglevel=info

Keep these processes running in separate terminal windows. The Celery worker will pick up tasks (like sending emails on order status changes) as they are dispatched.


API Documentation

The API is documented using Swagger UI (provided by drf-yasg). Once the server is running (via Docker or manual runserver), you can visit /swagger/ to view the interactive documentation for all API endpoints. This allows you to test API calls directly from the browser.

If ReDoc documentation is enabled, it would be accessible at /redoc/ for an alternative API docs view. (Redoc provides a more text-based documentation style.) Both documentation pages are automatically generated from the API schema.

Note: You may need to be authenticated to view the docs if the schema view is restricted. Logging in via the admin or obtaining a JWT token and providing it in the Swagger UI "Authorize" section will allow access to protected endpoints in the docs.

Running Tests

This project includes a test suite (unit tests) to ensure that major functionalities work as expected. To run the tests, use the following command:

python manage.py test

This will execute all tests across the apps. Ensure that you have applied migrations and set up any necessary test configuration (the tests may use the default SQLite database or the configured database depending on Django settings).

License

This project is open-sourced under the MIT License. Feel free to use, modify, and distribute this project in accordance with the terms of the license.

Maintainer

Name: Hamed Abbasgholizadeh
Email: hamedabbasgholi33@gmail.com
GitHub: github.com/hamedgholizade
