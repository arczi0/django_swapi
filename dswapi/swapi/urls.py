from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page),
    path('test/', views.home_screen_view),
    path('test/csv_preview/<str:filename>/', views.preview_downloaded_csv),
    path('load_more/', views.load_more, name='load_more')

]
