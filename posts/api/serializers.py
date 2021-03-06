from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField,

	)

from posts.models import Post

#comments
from comments.models import Comment
from comments.api.serializers import CommentSerializer
#UserDetail
from accounts.api.serializers import UserDetailSerializer


post_detail_url=HyperlinkedIdentityField(
		view_name='posts-api:detail',
		lookup_field='slug'
		)


class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model=Post
		fields=[
			
			'title',
			'content', 
			'publish',

		]

class PostDetailSerializer(ModelSerializer):

	user=UserDetailSerializer(read_only=True)
	image=SerializerMethodField()
	html=SerializerMethodField()
	comments=SerializerMethodField()
	class Meta:
		model=Post
		fields=[
			'id',
			'user',
			'title',
			'slug',
			'content', 
			'html',
			'publish',
			'image',
			'comments',

		]
	# def get_user(self,obj):         #get_fieldname
	# 	return obj.user.username	

	def get_html(self,obj):
		return obj.get_markdown()		

	def get_image(self,obj):
		try:
			image=obj.image.url
		except:
			image=None
		return image		

	def get_comments(self,obj):
		content_type=obj.get_content_type
		object_id=obj.id
		#c_qs=Comment.objects.filter(content_type=content_type,object_id=obj_id).filter(parent=None)
		c_qs=Comment.objects.filter_by_instance(obj)
		comments=CommentSerializer(c_qs,many=True).data
		return comments

class PostListSerializer(ModelSerializer):

	url=post_detail_url	
	user=SerializerMethodField()
	class Meta:
		model=Post
		fields=[
			'url',
			'user',
			'title',
			'content', 
			'publish',


		]

	def get_user(self,obj):         #get_fieldname
		return obj.user.username				