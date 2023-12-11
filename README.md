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
   git clone https://github.com/yourusername/friend-request-api.git
   cd friend-request-api

Create a virtual environment (optional but recommended):

bash
Copy code
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy code
venv\Scripts\activate
On macOS/Linux:

bash
Copy code
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Apply database migrations:

bash
Copy code
python manage.py migrate
Create a superuser (for accessing the Django admin):

bash
Copy code
python manage.py createsuperuser
Follow the prompts to create a superuser account.

Usage
Run the development server:

bash
Copy code
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