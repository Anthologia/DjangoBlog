from django.contrib import admin
from django.urls import path, include
import BlogApp.urls
import account.urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BlogApp.views.home, name = "home"),
    path('blog/', include(BlogApp.urls)),
    path('account/', include(account.urls)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
