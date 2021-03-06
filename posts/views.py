from django.http import HttpResponse,Http404
from .models import Post
from .forms import PostForm
from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.contrib import messages
#pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
#for encoded url
from urllib import quote_plus
#timezone
from django.utils import timezone
#Q lookups
from django.db.models import Q
#Comments
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType

# Create your views here.

from django.template.context import RequestContext


def post_create(request):

	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form=PostForm(request.POST or None,request.FILES or None)
	if request.method=="POST":

		if form.is_valid():
			instance=form.save(commit=False)
			instance.user=request.user
			print request.POST.get("title")
			print form.cleaned_data["title"]
			instance.save()
			messages.success(request,"Successfully Created")
			return redirect("posts:create")
		else:
			messages.error(request,"Not Successfully Created")


	return render(request,"post_form.html",{"form":form})


def post_detail(request,slug):

	instance=get_object_or_404(Post,slug=slug)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string=quote_plus(instance.content)
	comments=instance.comments
	initial_data={
	"content_type":instance.get_content_type,
	"object_id":instance.id
	}
	form=CommentForm(request.POST or None,initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type=form.cleaned_data["content_type"]
		content_type=ContentType.objects.get(model=c_type)
		obj_id=form.cleaned_data["object_id"]
		content_data=form.cleaned_data["content"]
		parent_obj=None
		try:
			parent_id=int(request.POST.get("parent_id"))
		except:
			parent_id=None

		if parent_id:
			parent_qs=Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count()==1:
				parent_obj=parent_qs.first()		
		new_comment, created=Comment.objects.get_or_create(
								user=request.user,
								content_type=content_type,
								object_id=obj_id,
								content=content_data,
								parent=parent_obj,
								)
		return redirect(new_comment.content_object.get_absolute_url())
		
	context={
	"title":"Detail Page",
	"instance":instance,
	"share_string":share_string,
	"comments":comments,
	"comment_form":form,

	}
	return render(request,"post_detail.html",context)

def post_list(request):
	today=timezone.now().date()
	queryset_list=Post.objects.active() #.order_by("-timestamp")

	query=request.GET.get("q")

	if request.user.is_staff or request.user.is_superuser:
		queryset_list=Post.objects.all()
	if query:
		queryset_list=queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query)
			).distinct()
	paginator = Paginator(queryset_list, 2) # Show 25 contacts per page
	page_request_var='page'
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context={
	"title":"Home Page",
	"queryset":queryset,
	"page_request_var":page_request_var,
	"today":today,

	}
	if request.is_ajax():
		return render(request,"results.html",context)
	return render(request,"post_list.html",context)


def post_update(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
		
	instance=get_object_or_404(Post,slug=slug)
	form=PostForm(request.POST or None,request.FILES or None,instance=instance)
	
	if request.method=="POST":
		if form.is_valid():
			instance=form.save(commit=False)
			instance.save()
			messages.success(request,"<a href='#'>Item</a>Successfully Updated",extra_tags="html_safe")
			return redirect(instance.get_absolute_url())
		else:
			messages.error(request,"Not Successfully Updated")
			
	context={
	"title":"Detail Page",
	"instance":instance,
	"form":form,

	}

	return render(request,"post_form.html",context)


def post_delete(request,slug=None):
	instance=get_object_or_404(Post,slug=slug)
	instance.delete()
	messages.success(request,"Successfully deleted")
	print "Successfully deleted"
	return redirect("posts:home")

