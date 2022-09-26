from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    list_display = ( 'title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    summernote_fields = ('content')

# admin.site.register(Post)

# Manually adding a slug field each time quickly becomes tedious. So we can use a "prepopulated_field" in the admin to 
# automate the process for us: when we enter the post title, we want the  slug field to be generated automatically.  
# To do that, we'll use the  prepopulated_fields property, Which was specifically designed for generating slug fields.. 
# To  use it, we pass in a dictionary that maps the field names to the fields that we want to  
# populate from. In our case, we want to populate the slug field from the title field. So above  
# my summernote_fields property here, we add "prepopulated_fields =" then my Python dictionary, we're populating slug from title

# list_filter creates filter box on the right hand side that allows me to filter the posts by  their status or by the created date.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'approved') 
    list_filter = ('approved', 'created_on')
    search_fields = ['name', 'email', 'body']
    actions = ['approve_comments']

    # create our approve_comments method.
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


# ACTION allows us to approve the comment: 
# In our model, the approved field is set to false by default. This ensures that all comments  
# need to be manually approved by an admin before they appear on the site. So now we want to add the  
# approval action to the admin site. 
# 
# To do this, we use another handy  built-in feature of the admin classes, which is actions. The actions 
# method allows you to specify different actions that can be  performed from the action drop-down box. 
# Now the default action is just  to delete the selected items but we want to add an approved comment section 
# too. So to do this, at the bottom of our class we'll add, "actions = ['approve_comments']".

# the approved field is a  boolean field that's set to false by default,  
# to approve the comment we just need to  set that field to true.  
# queryset is the one that we use to update our record: we just call the 
# update method on the query set and change our approved field to true