from django.urls import path
from .views import UserProfileList, CSVDataView

urlpatterns = [
    path('', UserProfileList.as_view(), name='user-profile-list'),
    path('csv/', CSVDataView.as_view(), name='csv-data'),  # Removed <str:file_path> from the URL pattern
] 