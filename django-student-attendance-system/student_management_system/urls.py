from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from student_management_system import settings

urlpatterns = [
    path('admin/', admin.site.urls),                 # Django Admin
    path('', include('student_management_app.urls')) # Main App
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
