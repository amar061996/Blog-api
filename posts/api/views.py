#class based views
from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,

	)
#rest framework permissions
from rest_framework.permissions import (
	AllowAny,
	IsAdminUser,
	IsAuthenticated,
	IsAuthenticatedOrReadOnly,


	)
#custom permissions
from .permissions import IsOwnerOrReadOnly

from posts.models import Post
#serializer
from .serializers import (
	PostCreateUpdateSerializer,
	PostDetailSerializer,
	PostListSerializer ,
	)
#rest framework inbuilt filters
from rest_framework.filters import (
		SearchFilter,
		OrderingFilter,


	)
#built-in pagination
from rest_framework.pagination import (
		PageNumberPagination,
		LimitOffsetPagination,

	)
#custom pagination
from .pagination import PostListOffsetPagination,PostPageNumberPagination
#Q lookups
from django.db.models import Q

class PostCreateAPIView(CreateAPIView):

	queryset=Post.objects.all()
	serializer_class=PostCreateUpdateSerializer
	permission_classes=[IsAdminUser,IsAuthenticated]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)

class PostListAPIView(ListAPIView):

	#queryset=Post.objects.all()			use when not overriding get_queryset
	serializer_class=PostListSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields=['title','content','user__first_name']
	pagination_class=PostPageNumberPagination
	#override get_queryset
	def get_queryset(self,*args,**kwargs):

		queryset_list=Post.objects.all()     # or super(PostListAPIView,self).get_queryset(*args,**kwargs)
		query=self.request.GET.get("q")

		if query:
			queryset_list=queryset_list.filter(
				Q(title__icontains=query) |
				Q(content__icontains=query) |
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
		return queryset_list		

class PostUpdatetAPIView(RetrieveUpdateAPIView):

	queryset=Post.objects.all()
	serializer_class=PostCreateUpdateSerializer
	lookup_field='slug'     #default is pk
	permission_classes=[IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


	def perform_update(self,serializer):
		serializer.save(user=self.request.user)
		

class PostDeleteAPIView(DestroyAPIView):

	queryset=Post.objects.all()
	serializer_class=PostListSerializer
	lookup_field='slug'     #default is pk
	permission_classes=[IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class PostDetailAPIView(RetrieveAPIView):

	queryset=Post.objects.all()
	serializer_class=PostDetailSerializer
	lookup_field='slug'     #default is pk
	#lookup_url_kwarg='abc' #kw name to be specified in url