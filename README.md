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

### Special APIs
- `GET /api/patient-status/?name={name}` - Get current status of a patient
- `GET /api/patient-visits/?name={name}&start_date={date}&end_date={date}` - Get patient visit history

## Technology Stack

- Django
- Django REST Framework
- SQLite Database
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

