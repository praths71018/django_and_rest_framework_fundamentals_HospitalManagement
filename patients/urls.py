from django.urls import path
from .views import PatientListView, PatientDetailView

urlpatterns = [
    path('', PatientListView.as_view(), name='patient-list'),
    path('<int:patient_id>/', PatientDetailView.as_view(), name='patient-detail'),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.patient_list, name='patient-list'),
#     path('<int:patient_id>/', views.patient_detail, name='patient-detail'),
# ]
