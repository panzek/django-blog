from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

# create a tuple for our status, which is going to be a 
# zero for draft post or a one for a published post. 
STATUS = ((0, 'Draft'), (1, 'Published'))

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

# "on_delete=models.CASCADE" that we have in our ForeignKey means that if the one record  
# in our one-to-many relationship is deleted, then the related records will be deleted too.
# In other words, if we delete our user  we'll also delete their blog posts.

# our updated on date is going to be a simple Django model date time 
# field, and it will automatically default to the current date and time. 

# our featured image is going to be a Cloudinary field. We give it a type, which is image. 
# And we'll also set a placeholder here which is just going to be set to placeholder

# our "created_on" will be a standard date time field, and that will 
# automatically default to the current time when it's been created.

# our status is going to be an integer field because it can be zero or one, and 
# the choices are going to be our status that we created above and the 
# default is going to be zero so the default will be draft.

# our likes is a many-to-many field, this is also going to pull from our 
# user. Related name is going to be blog likes and it can also be blank.
    class Meta:
        ordering = ['-created_on']
        # In this instance, we're going to order  our posts on the created_on field,  
        # now the minus sign means to use descending order.
    
    def __str__(self):
        return self.title
        # we use this "___str__() string method" here, it's good practice to put that into your projects.

        # Whenever an instance of model is created in Django, it displays the object as “ModelName Object(1).” 
        # To change the display name, we use "def __str__() method" in a model. str function in a django 
        # model returns a string that is exactly rendered as the "display name" of instances for that model.
    
    def number_of_likes(self):
        return self.likes.count()
        # a helper method to return the total number of likes on a post.

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80, unique=True)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']
        # This time we've ordered by created_on in ascending order, so that the oldest comments 
        # will be listed first which makes sense since we want this to be a conversation.

    def __str__(self):
        return f"comment {self.body}, {self.name}"
        # set __str__ which is Django best practice.

# we then migrate these changes into our database:
# 1. Test first: "python3 manage.py makemigrations --dry-run"
# 2. Make migration: "python3 manage.py makemigrations" 
# 3. Then migrate: "python3 manage.py migrate".