from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("<slug:slug>", views.PostDetail.as_view(), name="post_detail"),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]

# note again that this "url.py" is different from the main "urls.py" Django created 
# for us inside the xclusive_blog folder when we run the startproject command.

# import  our views 
# "import path" because we need that from django.urls 
# create a URL pattern for our home page. 
# we supply our path, and just supply a blank path because that indicates that it's our default, our home page.
# "("", views.PostList.as_view(), name="home")" is similar to what you've done before, but because we're using 
# class-based views we need to add the as_view method on the end of post list. So it's going to render this class as a view.

# Now, we just need to import these URLs in our main "xclusive_blog" URLs file.
# Go to the "xclusive_blog" directory, after our Summernote path, add in a blank path indicating our home page.  
# We'll include our blog directory dot URLs file, and we'll give this the name of "blog_urls".

# the first slug in angle brackets is called a path converter.The second slog is a keyword name, which mataches 
# the "slug" parameter in the get method of the PostDetail class in the blog/views.py file. That's how we link them together.

# In sum, the path converter converts this text into a slug  field, it tells Django to match any slug 
# string, which consists of ASCII characters or numbers  plus the hyphen and underscore characters.
# There are a number of these helpful path converters, which allow you to match numbers, or strings, or characters. 
# This means that our posts will have friendly URLs that consist of our  Heroku project URL followed by the slug.

# The final thing that we need to do then is to add the post detail URL into our index.html file, 
# so that users can click on the title  or the excerpt and read the post.
