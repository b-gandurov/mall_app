from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mall_app.users.urls')),
    path('parking/', include('mall_app.parking.urls')),
    path('cinema/', include('mall_app.cinema.urls')),
    path('stores/', include('mall_app.stores.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

