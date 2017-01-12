from django.conf.urls import url
import views as thread_views
urlpatterns = [
    
    
    
    url(r'^(?P<pk>\d+)/$',thread_views.comment_thread,name="thread"),
    
    url(r'^(?P<pk>\d+)/delete/$',thread_views.comment_delete,name="delete"),

]
