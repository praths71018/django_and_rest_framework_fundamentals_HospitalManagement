from django.urls import path
from .views import MedicineListView, MedicineDetailView

urlpatterns = [
    path('', MedicineListView.as_view(), name='medicine-list'),
    path('<int:medicine_id>/', MedicineDetailView.as_view(), name='medicine-detail'),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.medicine_list, name='medicine-list'),
#     path('<int:pk>/', views.medicine_detail, name='medicine-detail'),
# ]
