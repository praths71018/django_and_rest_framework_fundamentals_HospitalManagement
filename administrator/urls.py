from django.urls import path
from .views import (
    AdministratorListView, 
    AdministratorDetailView,
    HospitalDetailView,
    DepartmentDetailView
)

urlpatterns = [
    path('', AdministratorListView.as_view(), name='administrator-list'),
    path('<int:admin_id>/', AdministratorDetailView.as_view(), name='administrator-detail'),
    path('<int:hospital_id>/', HospitalDetailView.as_view(), name='hospital-detail'),
    path('<int:dept_id>/', DepartmentDetailView.as_view(), name='department-detail'),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.administrator_list, name='administrator-list'),
#     path('<int:admin_id>/', views.administrator_detail, name='administrator-detail'),
#     path('hospitals/<int:hospital_id>/', views.hospital_detail, name='hospital-detail'),
#     path('departments/<int:dept_id>/', views.department_detail, name='department-detail'),
# ]
