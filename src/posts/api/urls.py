from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^all$', views.PostListAllAPIView.as_view(), name='api_socialwall_all'),
]
