from django.shortcuts import render,get_object_or_404,redirect

#Comments Model
from .models import Comment
#Comment Form
from .forms import CommentForm
#ContentType
from django.contrib.contenttypes.models import ContentType
#messages
from django.contrib import messages
#http
from django.http import Http404,HttpResponse
#login required decorator
from django.contrib.auth.decorators import login_required
# Create your views here.

def comment_thread(request,pk):
	#obj=get_object_or_404(Comment,id=pk)
	try:
		obj=Comment.objects.get(id=pk)
	except:
		raise Http404	

	if not obj.is_parent:
		obj=obj.parent	
	initial_data={
	"content_type":obj.content_type,
	"object_id":obj.object_id
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
	"comment":obj,
	"form":form,
	}
	return render(request,"comment_thread.html",context)

@login_required(login_url='/login/')
def comment_delete(request,pk):
	#obj=get_object_or_404(Comment,id=pk)
	try:
		obj=Comment.objects.get(id=pk)
	except:
		raise Http404	

	if request.user!=obj.user:
		response=HttpResponse("You do not have permission to delete this")
		response.status_code=403
		return response
	if request.method=="POST":
		parent_object_url=obj.content_object.get_absolute_url()
		obj.delete()
		messages.success(request,"Successfully deleted")
		return redirect(parent_object_url)

	context={

	"object":obj,
	}
	return render(request,"confirm_delete.html",context)
