from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin),
    url(r'^register$', views.register),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^logoff$', views.logoff),
    url(r'^dashboard$', views.dashboard),
    url(r'^users/show/(?P<user_id>\d+)$', views.show),
    url(r'^users/message/(?P<user_id>\d+)$', views.message),
    url(r'^users/comment/(?P<user_id>\d+)/(?P<message_id>\d+)$', views.comment),
    url(r'^users/edit$', views.edit),
    url(r'^users/update_info/(?P<user_id>\d+)$', views.update_info),
    url(r'^users/update_password/(?P<user_id>\d+)$', views.update_password),
    url(r'^users/description/(?P<user_id>\d+)$', views.description),
    url(r'^dashboard/admin$', views.admin_dashboard),
    url(r'^users/edit/(?P<user_id>\d+)$', views.admin_edit),
    url(r'^users/delete/(?P<user_id>\d+)$', views.delete),
    url(r'^add$', views.add),
    url(r'^new$', views.new),
]
