from django.urls import path
from .views import CreateAlertView, DeleteAlertView, AlertListView

urlpatterns = [
    path('create/', CreateAlertView.as_view(), name='create-alert'),
    path('delete/<int:pk>/', DeleteAlertView.as_view(), name='delete-alert'),
    path('list/', AlertListView.as_view(), name='list-alerts'),
]