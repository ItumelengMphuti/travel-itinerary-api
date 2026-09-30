# Travel Itinerary Planning & Booking API

A Django REST Framework API for planning, managing, and collaborating on travel itineraries.

The API allows users to create travel itineraries, explore destinations, manage bookings and expenses, create budgets, share trips with other users, and leave destination reviews.

## Features

* User registration and profile management
* JWT authentication
* Destination browsing, searching, filtering, and ordering
* Destination recommendations and popular destinations
* Custom travel itinerary creation
* Itinerary collaboration and participant management
* Itinerary cover image uploads
* Accommodation bookings
* Activity bookings
* Travel budgets
* Trip expense tracking
* Destination reviews
* Object-level permissions
* Filtering, searching, ordering, and pagination
* Optimized database queries
* Swagger and ReDoc API documentation

## Technology Stack

* **Python**
* **Django**
* **Django REST Framework**
* **Simple JWT**
* **django-filter**
* **drf-spectacular**
* **Pillow**
* **SQLite** for development
* **pytest / Django TestCase** for testing

## Project Structure

```text
travel-itinerary-api/
│
├── travel_api/
│   ├── accounts/
│   ├── destinations/
│   ├── itineraries/
│   ├── bookings/
│   ├── budgets/
│   ├── reviews/
│   │
│   ├── travel_api/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── manage.py
│   └── requirements.txt
│
├── .env.example
├── .gitignore
└── README.md
```

## Installation

Clone the repository and move into the project directory:

```bash
git clone https://github.com/ItumelengMphuti/travel-itinerary-api
cd travel-itinerary-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example` as a template.

Example:

```text
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

Run migrations:

```bash
python manage.py migrate
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Authentication

The API uses **JWT authentication**.

### Obtain a token

```http
POST /api/auth/token/
```

Example request:

```json
{
    "username": "john",
    "password": "password123"
}
```

The response contains an access token and refresh token.

Use the access token in authenticated requests:

```text
Authorization: Bearer <access_token>
```

### Refresh a token

```http
POST /api/auth/token/refresh/
```

## API Documentation

Interactive API documentation is available through Swagger:

```text
/api/docs/
```

The OpenAPI schema is available at:

```text
/api/schema/
```

ReDoc is available at:

```text
/api/redoc/
```

## Main API Endpoints

### Authentication

| Method    | Endpoint                     | Description              |
| --------- | ---------------------------- | ------------------------ |
| POST      | `/api/auth/register/`        | Register a user          |
| GET       | `/api/auth/profile/`         | View current profile     |
| PUT/PATCH | `/api/auth/profile/update/`  | Update profile           |
| PUT/PATCH | `/api/auth/password/change/` | Change password          |
| POST      | `/api/auth/token/`           | Obtain JWT tokens        |
| POST      | `/api/auth/token/refresh/`   | Refresh JWT access token |

### Destinations

| Method    | Endpoint                                | Description                 |
| --------- | --------------------------------------- | --------------------------- |
| GET       | `/api/v1/destinations/`                 | List destinations           |
| POST      | `/api/v1/destinations/`                 | Create a destination        |
| GET       | `/api/v1/destinations/{id}/`            | Retrieve a destination      |
| PUT/PATCH | `/api/v1/destinations/{id}/`            | Update a destination        |
| DELETE    | `/api/v1/destinations/{id}/`            | Delete a destination        |
| GET       | `/api/v1/destinations/{id}/reviews/`    | View destination reviews    |
| GET       | `/api/v1/destinations/recommendations/` | Get recommendations         |
| GET       | `/api/v1/destinations/popular/`         | Get popular destinations    |
| GET       | `/api/v1/destinations/statistics/`      | View destination statistics |

### Itineraries

| Method    | Endpoint                                 | Description                         |
| --------- | ---------------------------------------- | ----------------------------------- |
| GET       | `/api/v1/itineraries/`                   | List itineraries                    |
| POST      | `/api/v1/itineraries/`                   | Create an itinerary                 |
| GET       | `/api/v1/itineraries/{id}/`              | Retrieve an itinerary               |
| PUT/PATCH | `/api/v1/itineraries/{id}/`              | Update an itinerary                 |
| DELETE    | `/api/v1/itineraries/{id}/`              | Delete an itinerary                 |
| GET       | `/api/v1/itineraries/{id}/share/`        | Get shareable itinerary information |
| GET       | `/api/v1/itineraries/{id}/participants/` | View itinerary participants         |
| POST      | `/api/v1/itineraries/{id}/upload_cover/` | Upload an itinerary cover image     |

### Bookings

| Method               | Endpoint                               | Description                             |
| -------------------- | -------------------------------------- | --------------------------------------- |
| GET/POST             | `/api/v1/accommodation-bookings/`      | Manage accommodation bookings           |
| GET/PUT/PATCH/DELETE | `/api/v1/accommodation-bookings/{id}/` | Manage a specific accommodation booking |
| GET/POST             | `/api/v1/activity-bookings/`           | Manage activity bookings                |
| GET/PUT/PATCH/DELETE | `/api/v1/activity-bookings/{id}/`      | Manage a specific activity booking      |

### Budgets and Expenses

| Method               | Endpoint                        | Description               |
| -------------------- | ------------------------------- | ------------------------- |
| GET/POST             | `/api/v1/budgets/`              | Manage travel budgets     |
| GET/PUT/PATCH/DELETE | `/api/v1/budgets/{id}/`         | Manage a specific budget  |
| GET                  | `/api/v1/budgets/{id}/summary/` | View budget summary       |
| GET/POST             | `/api/v1/expenses/`             | Manage trip expenses      |
| GET/PUT/PATCH/DELETE | `/api/v1/expenses/{id}/`        | Manage a specific expense |

### Reviews

| Method               | Endpoint                | Description            |
| -------------------- | ----------------------- | ---------------------- |
| GET/POST             | `/api/v1/reviews/`      | List or create reviews |
| GET/PUT/PATCH/DELETE | `/api/v1/reviews/{id}/` | Manage a review        |

## Filtering, Searching and Ordering

The API supports filtering, searching, and ordering on supported endpoints.

Examples:

```text
/api/v1/destinations/?country=South Africa
```

Search:

```text
/api/v1/destinations/?search=Cape Town
```

Ordering:

```text
/api/v1/destinations/?ordering=-average_rating
```

Itineraries can also be filtered by status and dates.

Pagination is enabled globally with a default page size of 10 results.

## Permissions

The API uses authentication and object-level permissions to protect user data.

Custom permissions include:

* `IsOwnerOrReadOnly`
* `IsItineraryOwner`
* `IsItineraryParticipant`
* `IsOwnerOrParticipant`

Users can access their own resources while collaborative itinerary resources can also be accessed by authorised participants.

## Database Design

The project contains models for:

* Users
* Categories
* Destinations
* Itineraries
* Itinerary participants
* Accommodation bookings
* Activity bookings
* Budgets
* Trip expenses
* Reviews

The models use relationships including:

* ForeignKey
* Many-to-Many
* Through models
* One-to-One relationships

Database indexes and validation are used to improve query performance and protect data integrity.

## Query Optimization

The API uses Django ORM optimization techniques including:

* `select_related()`
* `prefetch_related()`
* `distinct()`
* Aggregation with `Avg()` and `Count()`

These techniques reduce unnecessary database queries when retrieving related objects.

## Testing

The project uses Django's testing tools and REST Framework's API testing utilities.

Tests cover:

* Models
* Serializers
* API views and ViewSets
* Authentication
* Permissions
* API endpoints
* Custom ViewSet actions

Run the test suite with:

```bash
python manage.py test
```

The current test suite contains **44 passing tests**.

To measure coverage:

```bash
coverage run manage.py test
coverage report
```

## Media Uploads

The API supports image uploads for destinations and itinerary cover images.

Uploaded media is stored in the configured media directory during development.

The itinerary cover upload endpoint accepts:

```text
POST /api/v1/itineraries/{id}/upload_cover/
```

using the `cover_image` form-data field.

## API Versioning

The primary API endpoints are available under:

```text
/api/v1/
```

The project also retains the original `/api/` routes for backwards compatibility.

## Development

Run Django's system checks before making changes:

```bash
python manage.py check
```

Create migrations after model changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

Run tests:

```bash
python manage.py test
```

Start the development server:

```bash
python manage.py runserver
```

## License

This project was developed as part of a software development capstone project.
