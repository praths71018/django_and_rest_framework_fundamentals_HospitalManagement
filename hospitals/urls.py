from django.urls import path
from .views import HospitalListView, HospitalDetailView

urlpatterns = [
    path('', HospitalListView.as_view(), name='hospital-list'),
    path('<int:pk>/', HospitalDetailView.as_view(), name='hospital-detail'),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.hospital_list, name='hospital-list'),
#     path('<int:pk>/', views.hospital_detail, name='hospital-detail'),
# ]
