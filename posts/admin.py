from django.contrib import admin

# Register your models here.
from .models import Post

#PostModelAdmin
class PostAdmin(admin.ModelAdmin):
	class Meta:
		model=Post

	list_display=["__unicode__","timestamp","updated"]	
	list_display_links=["__unicode__","updated"]
	list_filter=["updated","timestamp"]
	search_fields=["title","content"]

admin.site.register(Post,PostAdmin)