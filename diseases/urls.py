from django.urls import path
from .views import DiseaseListView, DiseaseDetailView

urlpatterns = [
    path('', DiseaseListView.as_view(), name='disease-list'),
    path('<int:pk>/', DiseaseDetailView.as_view(), name='disease-detail'),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.disease_list, name='disease-list'),
#     path('<int:disease_id>/', views.disease_detail, name='disease-detail'),
# ]
