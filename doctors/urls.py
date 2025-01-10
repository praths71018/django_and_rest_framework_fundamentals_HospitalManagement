from django.urls import path
from .views import DoctorListView, DoctorDetailView

urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     # Handles GET (list) and POST (create)
#     path('', views.doctor_list, name='doctor-list'),
    
#     # Handles PUT (update) and DELETE
#     path('<int:pk>/', views.doctor_detail, name='doctor-detail'),
# ]
