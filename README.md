# Hospital Management System

A comprehensive REST API-based hospital management system built with Django REST Framework.

## Project Overview

This system manages hospitals, departments, administrators, doctors, patients, medicines, and diseases through a set of interconnected REST APIs.

## Features

### 1. Hospital Management
- Create and manage multiple hospitals
- Track hospital details including name, address
- View all hospitals in the system

### 2. Department Management
- Create departments within hospitals
- Assign administrators to departments
- Track department-specific information

### 3. Administrator Management
- Administrators can manage multiple departments
- Each administrator is associated with a specific hospital
- Track administrator details and permissions

### 4. Doctor Management
- Manage doctors across different departments
- Track doctor specializations and status
- Associate doctors with specific hospitals and departments

### 5. Patient Management
- Track patient visits and medical history
- Associate patients with doctors
- Manage patient status (admitted/discharged/waiting)
- Record treatments and medications

### 6. Medicine & Disease Tracking
- Maintain medicine database
- Track diseases and their treatments
- Associate medicines with patients

## API Endpoints

### Hospitals
- `GET /hospitals/` - List all hospitals
- `POST /hospitals/` - Create new hospital
- `GET /hospitals/{id}/` - Get hospital details
- `PUT /hospitals/{id}/` - Update hospital
- `DELETE /hospitals/{id}/` - Delete hospital

### Departments
- `GET /departments/` - List all departments
- `POST /departments/` - Create new department
- `GET /departments/{id}/` - Get department details
- `PUT /departments/{id}/` - Update department
- `DELETE /departments/{id}/` - Delete department

### Administrators
- `GET /administrators/` - List all administrators
- `POST /administrators/` - Create new administrator
- `GET /administrators/{id}/` - Get administrator details
- `PUT /administrators/{id}/` - Update administrator
- `DELETE /administrators/{id}/` - Delete administrator

### Doctors
- `GET /doctors/` - List all doctors
- `POST /doctors/` - Create new doctor
- `GET /doctors/{id}/` - Get doctor details
- `PUT /doctors/{id}/` - Update doctor
- `DELETE /doctors/{id}/` - Delete doctor

### Patients
- `GET /patients/` - List all patients
- `POST /patients/` - Create new patient
- `GET /patients/{id}/` - Get patient details
- `PUT /patients/{id}/` - Update patient
- `DELETE /patients/{id}/` - Delete patient

### Medicines
- `GET /medicines/` - List all medicines
- `POST /medicines/` - Create new medicine
- `GET /medicines/{medicine_id}/` - Get medicine details
- `PUT /medicines/{medicine_id}/` - Update medicine
- `DELETE /medicines/{medicine_id}/` - Delete medicine

### Diseases
- `GET /diseases/` - List all diseases
- `POST /diseases/` - Create new disease
- `GET /diseases/{disease_id}/` - Get disease details
- `PUT /diseases/{disease_id}/` - Update disease
- `DELETE /diseases/{disease_id}/` - Delete disease


### Special APIs
- `GET /api/patient-status/?name={name}` - Get current status of a patient
- `GET /api/patient-visits/?name={name}&start_date={date}&end_date={date}` - Get patient visit history

## Technology Stack

- Django
- Django REST Framework
- MySQL Database
- Python 3.x

## Installation & Setup

1. Clone the repository:
```bash
git clone https://bitbucket.org/hospital_management_pratham/hospital_management.git
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Run the server:
```bash
python manage.py runserver
```

## Database Setup

### MySQL Configuration

1. Install MySQL dependencies:
```bash
pip install mysqlclient
```

2. Create MySQL database:
```sql
CREATE DATABASE HospitalShadowfax;
USE HospitalShadowfax;
```


3. Update settings.py with MySQL configuration:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'HospitalShadowfax',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

4. Install MySQL Server:
   - **Windows**: Download and install MySQL Server from [MySQL Official Website](https://dev.mysql.com/downloads/mysql/)
   - **Ubuntu/Debian**:
     ```bash
     sudo apt update
     sudo apt install mysql-server
     sudo mysql_secure_installation
     ```
   - **macOS**:
     ```bash
     brew install mysql
     brew services start mysql
     ```

5. Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Verify connection:
```bash
python manage.py dbshell
```

### Common MySQL Commands

```sql

SHOW TABLES;

select * from hospitals_hospital;

select * from departments_department;

select * from administrator_administrator;

select * from doctors_doctor;

select * from medicine_medicine;

select * from diseases_disease;

select * from patients_patient;
```

## Database Schema

The system uses the following models:
- Hospital
- Department
- Administrator
- Doctor
- Patient
- Medicine
- Disease

Each model maintains appropriate relationships with other models through foreign keys and many-to-many relationships.

# Unit Testing in Django

- URL: https://www.youtube.com/watch?v=k7pf42xD4bw
- Define a test class in the test file
- Define a test method in the test class
- Use the assert statement to check the expected result
- Run the test using the test command
```bash
python manage.py test hospitals
```

# Django Signals

- URL: https://www.youtube.com/watch?v=a6zVm5UqOoo
- Signals are used to send notifications or perform actions when certain events occur in the database
- Use the `post_save` signal to send a notification when a model is saved
- Use the `post_delete` signal to send a notification when a model is deleted
- Use the `pre_save` signal to send a notification when a model is saved and see previous data
- Use the `pre_delete` signal to send a notification when a model is deleted and see previous data
- Modify the models.py file to add signals
- Template : in models.py file
```python
@receiver(pre_save, sender=Medicine)
def send_medicine_notification(sender, instance, **kwargs):
    if instance.medicine_id:  # Check if the medicine already exists (not a new instance)
        previous_instance = sender.objects.get(medicine_id=instance.medicine_id)
        print(f"Medicine updated: {instance.medicine_name}")
        print(f"Previous data: {previous_instance.medicine_name}")
```

# Token Authentication

- Token Authentication is used to authenticate the user

- In settings.py file, add the following:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

- Make an app for authentication
- Authentication app contains login and signup views.
- It uses a User model to store user details. Predefined user model is used provided by django.
- Define a serializer for the User model.
- Define a view for the login view.
- Define a view for the signup view.
- Define urls.py file for the authentication app.
- Then in administrator app, add the following to routes/urls you want to protect/authenticate at beginning of class:
```python
from rest_framework.permissions import IsAuthenticated
class YourClass(APIView):
permission_classes = [IsAuthenticated]
```
- In settings.py file, add the following:
```python
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken',
    ...
]
```

- Now go to url which is authenicated:
- It tells you to login
- Login first.
- It gives you a token
- Open postman and go to url which is authenicated
- Go to headers tab
- Copy the token and paste it in the authorization header in postman
  - Key: Authorization
  - Value: Token <token>
- Send request
- It will give you the response

# Celery

- URL: https://www.youtube.com/watch?v=JYQG7zlLJrE&t=445s
- Celery is used to send messages and tasks asynchronously. 
- It acts as a message broker between the application and the worker.
- Decrease the response time of the application
- Allows to perform tasks in the background
- Example: sending email to the patient when the patient is admitted
- Install celery:
```bash
pip install celery
```
- Install redis: (redis is used as the message broker)
```bash
brew install redis
```
- Run redis server:
```bash
redis-server
```

-  pip install redis 

- Configure celery:
 - In system create a file called celery.py
 - Add the following code:
```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<core>.settings')

app = Celery('<core>')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

- In settings.py file, add the following:
```python
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
```

- Add below code in __init__.py file of the app where you want to use celery:
```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```
- Create a file called tasks.py in the app where you want to use celery (patients):
```python
from celery import shared_task
from .models import Patient

@shared_task
def send_patient_email(email, message):
    print(f"Sending email to {email} with message: {message}")
```
- Then in views.py file, add the following code:
```python
from .tasks import send_patient_email  # Import the task to send email

class PatientListView(APIView):
    def post(self, request):
        data = request.data
        patient = Patient.objects.create(**data)
        send_patient_email.delay(patient.patient_id)  # Send email asynchronously
        return Response({"message": "Patient created and email sent"}, status=status.HTTP_201_CREATED)
```

- Add App password in settings.py file :
    - First go to google account settings and create app password (2 step verification should be enabled)
    - Then add the app password in settings.py file
    - Then add the email address in settings.py file


- Run celery worker:
```bash
celery -A system worker -l info
```

# Django Middleware

- URL: https://www.youtube.com/watch?v=A4PAJDkHJfI
- Middleware is used to process requests and responses
- Before a request is processed by views.py file , it is processed by middleware.
- Example: If authentication is enabled for the api/class , before it is processed by views.py file , it is processed by middleware.  ('django.contrib.auth.middlewareAuthenticationMiddleware', in settings.py file)
- Middleware is used to add custom headers to the request and response
- Middleware is called based on sequence in settings.py file i.e. in :
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
First security middleware is called , then session middleware is called , then common middleware is called , then csrf middleware is called , then authentication middleware is called and so on. Hence order is important.

- To create a middleware, create a folder called middleware in the app where you want to use it.
- Create a __init__.py file in the middleware folder.
- Create a main.py file in the middleware folder and add functions to it you want to execute before the request is processed by views.py file by any api/class.
- Add the middleware in settings.py file in MIDDLEWARE list.
- If you want to add middleware in only one api/class, add it in the class you want to protect as middleware.py file.

# Celery Beat

- URL: https://www.youtube.com/watch?v=JYQG7zlLJrE&t=445s
- Celery Beat is used to schedule tasks to run at a specific time.
- pip install django-celery-beat
- pip install django-celery-results
- Add the following in settings.py file:
```python
INSTALLED_APPS = [
    ...
    'django_celery_results',
    'django_celery_beat',
    ...
]
```
- In tasks.py file, create a function to send emails to all patients at a specific time.
- In celery.py file, add the following code:
```python
app.conf.beat_schedule = {
    'send-patient-details-every-day': {
        'task': 'patients.tasks.send_all_patients_email',
        'schedule': crontab(hour=14, minute=20),
    },
}
```
- Run the server:
```bash
python manage.py runserver
```
- Run celery worker:
```bash
celery -A system worker -l info
```
- Run celery beat:
```bash
celery -A system beat -l info
```

# Encryption

- URL: https://www.youtube.com/watch?v=AKa7VTZwLzQ
- pip install cryptography
- Create a file called encryption.py in the utils folder in the patients app
- Create encrypt and decrypt functions in the encryption.py file
- Open the terminal and run the following command to generate a key:
```bash
python manage.py shell
```
- Add the following code in the shell:
```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key)
```
- Copy the key and paste it in the ENCRYPT_KEY variable in the settings.py file
- In models.py file, add the following code:
```python
from .utils.encryption import encrypt, decrypt  # Import the encrypt and decrypt functions

def save(self, *args, **kwargs):
    # Encrypt the phone number before saving
    if self.phone:
        self.phone = encrypt(self.phone)
    super().save(*args, **kwargs)

def get_decrypted_phone(self):
    # Decrypt the phone number when retrieving
    return decrypt(self.phone) if self.phone else None
```
- Encrypt the phone number before saving and decrypt the phone number when retrieving in the views.py file

# APM using NewRelic

- Create a New Relic account
- Go to APM and Services and create a new application
- Copy the license key
- Download the New Relic Python Agent in the directory where the project is located
- Create a newrelic.ini file in the directory where the project is located (downloaded from newrelic)
- pip install newrelic
- In terminal run the following command:
```bash
   newrelic-admin generate-config YOUR_NEW_RELIC_LICENSE_KEY newrelic.ini
```
- Modify the wsgi.py file to include the newrelic.ini file
```python
import newrelic.agent
newrelic.agent.initialize('/Users/prathamshetty/Desktop/Shadowfax/Hospital/newrelic.ini')  # Update the path to your newrelic.ini file
```
- Run the server
```bash
   gunicorn system.wsgi:application
```
- Go to New Relic and see the application

# BitBucket Commands

## First time setup
- Goto the project directory
- git init
- git branch -m main
-  git remote add origin https://prathamshetty2@bitbucket.org/hospital_management_pratham/hospital_management.git
- git add --all
- git commit -m "Initial commit"


- Before pushing to bitbucket Go to personalised bitbucket settings and add app password for the repository
- generates password for the repository
- git push -u origin main

## Pushing to bitbucket
- git add --all
- git commit -m "commit message"
- git push

## Branching

- create a new branch:
```bash
git checkout -b <branch_name>
```
- push the branch to bitbucket:
```bash
git push -u origin <branch_name>
```
- merge the branch to main:
```bash
git checkout main
git merge <branch_name>
git push origin main
```
- delete the branch:
```bash
git branch -d <branch_name>
```
- Pull request to main branch:
- Go to bitbucket and create a pull request from the branch to main
- Merge the pull request
- Delete the branch
