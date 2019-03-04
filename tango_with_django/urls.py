from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.urls import RegistrationView

class MyRegistrationView(RegistrationView):
    success_url = '/rango/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rango/', include('rango.urls')),
    path('accounts/register/', MyRegistrationView.as_view(), name='registration_register'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('search/', include('search.urls', namespace='search')),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

