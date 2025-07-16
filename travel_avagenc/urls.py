from django.contrib import admin
from django.urls import path, include  # ← tambahkan include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # ← ini penting agar / diarahkan ke app 'main'
]
