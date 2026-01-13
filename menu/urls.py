from django.urls import path
from .views import MenuByQRView

urlpatterns = [
    path("menu/<uuid:qr_token>/", MenuByQRView.as_view()),
]