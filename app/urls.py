from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<service>[a-z]+)/(?P<year>[0-9]{4})$', views.get_report),
    url(r'^(?P<service>[a-z]+)/(?P<month>[0-9]+-[0-9]{4})$', views.get_report),
    url(r'^(?P<service>[a-z]+)/(?P<day>[0-9]+-[0-9]+-[0-9]{4})$', views.get_report),
    url(r'^(?P<service>[a-z]+)/(?P<when>[a-z]+)$', views.get_report),
    url(r'^(?P<service>[a-z]+)/last-(?P<days>[0-9]+)-days$', views.get_report_by_date_range),
    url(r'^(?P<service>[a-z]+)/(?P<_from>[0-9]+-[0-9]+-[0-9]{4})/(?P<to>[0-9]+-[0-9]+-[0-9]{4})$', views.get_report_by_date_range),
]