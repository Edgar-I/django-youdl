from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_downloader, name='show_converter'),
    path('convert/', views.convert_video, name='convert_video'),
    path('download/<int:video_id>/', views.download_video, name='download_video_by_id'),
]