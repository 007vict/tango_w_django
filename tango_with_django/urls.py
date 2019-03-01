from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.urls import RegistrationView


# class MyRegistrationView(RegistrationView):
#     def get_success_url(self, request, user):
#         return '/rango/'
class MyRegistrationView(RegistrationView):
    success_url = '/rango/'
    # def get_success_url(self, request, user):
    #     return '/rango/'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rango/', include('rango.urls')),
    path('accounts/register/', MyRegistrationView.as_view(), name='registration_register'),
    path('accounts/', include('registration.backends.simple.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
