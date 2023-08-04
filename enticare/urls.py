from django.urls import path
from .views import GeneratePDF



urlpatterns = [
    path('form/',GeneratePDF.as_view(),name="Form"),
]