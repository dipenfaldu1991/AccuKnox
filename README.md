# AccuKnox
# Friend Request System - Django REST API

This project implements a simple Friend Request System using Django REST Framework.

## Prerequisites

- Python (3.x recommended)
- Django
- Django REST Framework

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dipenfaldu1991/AccuKnox.git
   cd AccuKnox

Create a virtual environment (optional but recommended):
python -m venv venv
Activate the virtual environment:


On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate


Install dependencies:
pip install -r requirements.txt


Apply database migrations:
python manage.py migrate


Create a superuser (for accessing the Django admin):
python manage.py createsuperuser
Follow the prompts to create a superuser account.

Usage
Run the development server:
python manage.py runserver
The API will be accessible at http://127.0.0.1:8000/.


Access the Django admin interface:
Navigate to http://127.0.0.1:8000/admin/
Log in with the superuser credentials created earlier.
Create a few users and start sending, accepting, and rejecting friend requests using the API endpoints:



/account/api/register/ (POST): User register
/account/api/login/ (POST): User Login
/account/users/?keyword=dipen@gmail.com (GET): Search User
/account/api/friend-requests/ (POST): Send a friend request.
/account/api/friend-requests/5/accept_friend_request/ (PATCH): Accept a friend request.
/account/api/friend-requests/5/reject_friend_request/ (PATCH): Reject a friend request.
/account/api/friend-requests/friends/ (GET): List friends.
/account/api/friend-requests/pending_requests/ (GET): List pending friend requests.
