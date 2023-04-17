from django.urls import path
from . import views

app_name = 'file'
urlpatterns = [
    path('download/',  views.download_excel, name='download_excel'),
    path('import/',  views.import_excel, name='import_excel'),
    path('export/',  views.export_excel, name='export_excel'),
]