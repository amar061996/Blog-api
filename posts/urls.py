from django.conf.urls import url
import views as post_views

urlpatterns = [
    
    url(r'^$',post_views.post_list,name="home"),
    url(r'^create/$',post_views.post_create,name="create"),
    url(r'^(?P<slug>[\w-]+)/$',post_views.post_detail,name="detail"),
    url(r'^(?P<slug>[\w-]+)/edit/$',post_views.post_update,name="update"),
    url(r'^(?P<slug>[\w-]+)/delete/$',post_views.post_delete,name="delete"),

]
