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
#mixins
from rest_framework.mixins import (
	DestroyModelMixin,
	UpdateModelMixin,



	)
#custom permissions
from posts.api.permissions import IsOwnerOrReadOnly

from comments.models import Comment
#serializer
from .serializers import (
	CommentSerializer,
	CommentListSerializer,
	CommentDetailSerializer,
	create_comment_serializer,
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
from posts.api.pagination import PostListOffsetPagination,PostPageNumberPagination
#Q lookups
from django.db.models import Q

class CommentCreateAPIView(CreateAPIView):

	queryset=Comment.objects.all()
	# serializer_class=PostCreateUpdateSerializer
	permission_classes=[IsAuthenticated]

	def get_serializer_class(self):
		model_type=self.request.GET.get("type")
		slug=self.request.GET.get("slug")
		parent_id=self.request.GET.get("parent_id")
		print "parent id:",parent_id
		return create_comment_serializer(
			model_type=model_type,
			slug=slug,
			parent_id=parent_id,
			user=self.request.user)

	# def perform_create(self,serializer):
	# 	serializer.save(user=self.request.user)

class CommentListAPIView(ListAPIView):

	#queryset=Post.objects.all()			use when not overriding get_queryset
	serializer_class=CommentListSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields=['content','user__first_name']
	pagination_class=PostPageNumberPagination
	#override get_queryset
	def get_queryset(self,*args,**kwargs):

		# queryset_list=super(PostListAPIView,self).get_queryset(*args,**kwargs)
		queryset_list=Comment.objects.filter(id__gte=0)  #getting all comments     # or super(PostListAPIView,self).get_queryset(*args,**kwargs)
		query=self.request.GET.get("q")

		if query:
			queryset_list=queryset_list.filter(
				Q(content__icontains=query) |
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
		return queryset_list		


class CommentDetailAPIView(DestroyModelMixin,UpdateModelMixin,RetrieveAPIView):

	queryset=Comment.objects.filter(id__gte=0)
	serializer_class=CommentDetailSerializer
	permission_classes=[IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

	#update
	def put(self,request,*args,**kwargs):
		return self.update(request,*args,**kwargs)
	#delete
	def delete(self,request,*args,**kwargs):
		return self.destroy(request,*args,**kwargs)	





# class PostUpdatetAPIView(RetrieveUpdateAPIView):

# 	queryset=Post.objects.all()
# 	serializer_class=PostCreateUpdateSerializer
# 	lookup_field='slug'     #default is pk
# 	permission_classes=[IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# 	def perform_update(self,serializer):
# 		serializer.save(user=self.request.user)
		

# class PostDeleteAPIView(DestroyAPIView):

# 	queryset=Post.objects.all()
# 	serializer_class=PostListSerializer
# 	lookup_field='slug'     #default is pk
# 	permission_classes=[IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

