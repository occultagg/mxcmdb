from django.urls import path
from . import views

app_name = 'analyzer'
urlpatterns = [
    path('data/<int:days>', views.analyzer, name='analyzer'),
    ]
