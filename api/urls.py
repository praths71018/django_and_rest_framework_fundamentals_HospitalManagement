from django.urls import path
from .views import PatientStatusView, PatientVisitHistoryView

urlpatterns = [
    path('patient-status/', PatientStatusView.as_view(), name='patient-status'),
    path('patient-visits/', PatientVisitHistoryView.as_view(), name='patient-visits'),
] 