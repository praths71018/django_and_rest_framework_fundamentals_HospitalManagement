from django.urls import path
from .views import PatientListView, PatientDetailView, PatientStatusView, PatientVisitHistoryView

urlpatterns = [
    path('', PatientListView.as_view(), name='patient-list'),
    path('<int:patient_id>/', PatientDetailView.as_view(), name='patient-detail'),
    path('status/', PatientStatusView.as_view(), name='patient-status'),
    path('visit-history/', PatientVisitHistoryView.as_view(), name='patient-visit-history'),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.patient_list, name='patient-list'),
#     path('<int:patient_id>/', views.patient_detail, name='patient-detail'),
# ]
