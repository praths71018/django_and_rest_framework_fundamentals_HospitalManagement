from celery import shared_task
from .models import Patient
from django.core.mail import send_mail
from system.settings import EMAIL_HOST_USER

@shared_task()
def send_patient_email(patient_id):
    """Sends an email to the patient with their details."""
    patient = Patient.objects.get(patient_id=patient_id)  # Fetch the patient using the patient_id
    print(patient.email)
    message = (
        f"Dear {patient.patient_name},\n\n"
        f"Your status: {patient.status}\n"
        f"Medicine: {patient.medicine.medicine_name}\n"
        f"Disease: {patient.disease.disease_name}\n"
        f"Doctor: {patient.doctor.doctor_name}\n"
        f"Visit Time: {patient.visit_time}\n\n"
        "Thank you for choosing our services!"
    )
    
    send_mail(
        subject="Patient Details Confirmation",
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[patient.email],  # receiver email
        fail_silently=True, # if email fails to send, it will not raise an error hence won't affect the flow i.e. it will send other emails
    )
