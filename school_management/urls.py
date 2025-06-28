from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/staff/dashboard/', permanent=True)),  # Redirection par défaut
    path('admin/', admin.site.urls),
    path('staff/', include('staff.urls')),
    path('finance/', include('finance.urls')),
    path('administrative/', include('administrative.urls')),
    path('connexion/', include('users.urls')),
    path('deconnexion/', LogoutView.as_view(next_page='/staff/dashboard/'), name='logout'),
    path('communication/', include('communication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
