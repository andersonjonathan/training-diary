from django.urls import path
from .views import index, activity

urlpatterns = [
    path('', view=index, name="activities"),
    path('<int:pk>', view=activity, name="activity"),
]
