from django.urls import path
from .views import DepartmentListView, DepartmentDetailView

urlpatterns = [
    path('', DepartmentListView.as_view(), name='department-list'),
    path('<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.department_list, name='department-list'),
#     path('<int:pk>/', views.department_detail, name='department-detail'),
# ]
