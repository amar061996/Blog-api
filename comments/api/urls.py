from django.conf.urls import url


from . views import (
		CommentListAPIView,
		CommentDetailAPIView,
		CommentCreateAPIView,



	)
urlpatterns = [
    
    url(r'^$',CommentListAPIView.as_view(),name="list"),
	url(r'^create/$',CommentCreateAPIView.as_view(),name="create"),
    url(r'^(?P<pk>\d+)/$',CommentDetailAPIView.as_view(),name="thread"),

    
    # url(r'^(?P<pk>\d+)/delete/$',thread_views.comment_delete,name="delete"),

]
