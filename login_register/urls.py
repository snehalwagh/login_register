from django.conf.urls import patterns, include, url
from login_app import views
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import login, logout

urlpatterns = patterns(
    (r'^accounts/password/reset/$', password_reset),
    (r'^$', login),
    (r'^logout/$', views.logout_page),
    (r'^accounts/login/$', login),
    (r'^register/$', views.register),
    (r'^register/success/$', views.register_success),
    (r'^accounts/profile/$', views.home),
    (r'^home/$', views.home),
    (r'^activate/([a-zA-Z0-9_.-=]+)', views.activate_user),

)

