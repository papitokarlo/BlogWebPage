from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('account/', include('apps.authentication.urls')),
    path('blog/', include('apps.blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
