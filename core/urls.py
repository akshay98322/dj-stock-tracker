from django.urls import path
from . import views
urlpatterns = [
    path('', views.stockPicker, name='stock_picker'),
    path('stocktracker/', views.stockTracker, name='stock_tracker'),
]
