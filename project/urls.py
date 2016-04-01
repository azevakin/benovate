from django.conf.urls import patterns, include, url
from django.contrib import admin

from app.views import TransferView

urlpatterns = patterns('',
    url(r'^$', TransferView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
