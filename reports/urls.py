from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'', include('app.urls', namespace='app')),
    url(r'^admin/', admin.site.urls),
]