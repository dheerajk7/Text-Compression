from django.contrib import admin
from django.urls import path
from .import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('upload',views.upload,name='upload'),
    path('compression',views.compression,name='compression'),
    path('decompression',views.decompression,name='decompression'),
    path('contactus',views.contactus,name='contactus'),
    path('aboutus',views.aboutus,name='aboutus'),
 ]

if settings.DEBUG:
    urlpatterns = urlpatterns +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)