##Descriptions
This project is a Django Rest Framework API for a social networking application, allowing users to register, log in, search for other users, and send request, accept reject.

## Requirements
- Python 3.10.12
- Django 5.0.1
- Django REST Framework
- Postgres


## Installation
After you cloned the repository, you want to create a virtual environment
You can do this by running the command
```
python -m venv env
```
After this, it is necessary to activate the virtual environment, you can get more information about this [here](https://docs.python.org/3/tutorial/venv.html)

You can install all the required dependencies by running
```
pip install -r requirements.txt
```

#DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'your_host',
        'PORT': '5432',
    }
}

#api endpoint  |  CURD METHOD

http://localhost/api/signup/ | post
http://localhost/api/login/  | post
http://localhost/api/friend/list/ | get
http://localhost/api/user/search/ | get
http://localhost/api/friend/requests/ | get
http://localhost/api/friend/request/  | post
http://localhost/api/friend/accept/<int:pk>/ |put
http://localhost/api/friend/reject/<int:pk>/ |option

also postman file is share there you can get all data

for other than two apis which is signup and login  we need token for authorizations which we get from login api as output . we have to give that token to every api in postman as bearer token .