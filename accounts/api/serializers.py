from rest_framework.serializers import (
	CharField,
	EmailField,
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField,
	ValidationError

	)
from django.contrib.auth.models import User
from comments.models import Comment

from django.contrib.contenttypes.models import ContentType
#Q lookup
from django.db.models import Q



class UserDetailSerializer(ModelSerializer):
	class Meta:
		model=User
		fields=[
			'username',
			'email',
			'first_name',
			'last_name',

		]
class UserCreateSerializer(ModelSerializer):
	email2=EmailField(label='Confirm Email')
	class Meta:
		model=User
		fields=[
			'username',
			'email',
			'email2',
			'password',
			

		]

		extra_kwargs={"password":
							{"write_only":True }

					}
	#checking if email is already taken
	def validate(self,data):
		# email=data['email']
		# user_qs=User.objects.filter(email=email)
		# if user_qs.exists():
		# 	raise ValidationError("User already registered.")
		return data 					
	#validation for email
	def validate_email(self,value):
		data=self.get_initial()
		email1=data.get("email")				
		email2=value
		if email2!=email1:
			raise ValidationError("Emails must match")
		user_qs=User.objects.filter(email=email2)
		if user_qs.exists():
			raise ValidationError("User already registered.")	
		return value						
	#validation for email2
	def validate_email2(self,value):
		data=self.get_initial()
		email1=data.get("email")				
		email2=value
		if email2!=email1:
			raise ValidationError("Emails must match")

		return value	
	#overriding the create method
	def create(self,validated_data):
		username=validated_data['username']
		email=validated_data['email']
		password=validated_data['password']
		#create user
		user_obj=User(username=username,email=email)
		user_obj.set_password(password)
		user_obj.save()
		return validated_data


class UserLoginSerializer(ModelSerializer):
	username=CharField()
	email=EmailField(label='Email Address')
	token=CharField(allow_blank=True,read_only=True)
	class Meta:
		model=User
		fields=[
			'username',
			'email',
			'password',
			'token',
			

		]

		extra_kwargs={"password":
							{"write_only":True }

					}
	#checking if email is already taken
	def validate(self,data):
		user_obj=None
		email=data.get("email",None)
		username=data.egt("username",None)
		password=data.get("password",None)
		if not username or email:
			raise ValidationError("A username or email is required to login.")

		user=User.objects.filter(
					Q(username=username) |
					Q(email=email)
				).distinct()
		user=user.exclude(email__isnull=True).exclude(email__iexact='')
		if user.exists() and user.count()==1:
			user_obj=user.first()
		else:
			raise ValidationError("This username/email is not valid")
		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError("Incorrect credetials.Please try again.")

		data['token']="SOME RANDOM TOKEN"
		return data 			