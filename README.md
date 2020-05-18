# API
1. Login: 
Endpoint: /api/login
Type of request: POST
Body of request: username, password

2. Register:
	Endpoint: /api/register
  Type of Request: POST
  Body of request: username, email, fist_name, last_name, password1, password2


3. List of feeds:
 Endpoint: /api/feeds
Type of request: GET
Headers in request: Authorization Value: Token auth_token
Replace auth_token by the authorization token obtained when you login

# How to run this project

install all the dependencies from requirement.txt and then run manage.py using fololwing command

> python manage.py runserver --noreload --nothreading
