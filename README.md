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