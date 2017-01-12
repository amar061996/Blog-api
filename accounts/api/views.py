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

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
#custom permissions
from posts.api.permissions import IsOwnerOrReadOnly


from django.contrib.auth.models import User
#serializer
from .serializers import (
	UserCreateSerializer,
	UserLoginSerializer,
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

class UserCreateAPIView(CreateAPIView):
	serializer_class=UserCreateSerializer
	queryset=User.objects.all()

class UserLoginAPIView(APIView):
	permission_classes=[AllowAny]
	serializer_class=UserLoginSerializer
	#define post func
	def post(self,request,*args,**kwargs):
		data=request.data
		serializer=UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data=serializer.data
			return Response(new_data,status=HTTP_200_OK)

		return Response(serializer.errors,HTTP_400_BAD_REQUEST)		