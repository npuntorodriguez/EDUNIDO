from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1. Admin
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')), 
]