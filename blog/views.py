from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm

# Create post list view.
class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = "index.html"
    paginate_by = 6

# Create post list view.
class PostDetail(View):
    # GET method
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        return render(
            request, 
            'post_detail.html', 
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
            )
    
    # POST method
    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        # this will get all the data we posted from our form
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()
        
        return render(
            request, 
            'post_detail.html', 
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
            )
class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))





# for POST LIST VIEW
# import the generic library.
# import our Post model that will base our views on.
# we create our class called PostList and we're going to base this on the 
# generic "ListView" model, telling the class that it's inheriting from this.  

# Inside the class we're telling it to use Post as its model, and with that we can use 
# more of the built-in methods to quickly and easily render our "list of posts.""

# we supply the queryset here, which will be the contents of our Post table.  
# We filter this by status. Remember that our status field can be set to either 0  
# for draft, or one for published. We want only publish posts to be visible to the users,  
# so we'll filter our posts by status equals one and order them by created_on in descending order.  

# The template name is the html file that our view will render

# paginate means separate into pages. By setting paginate_by to six, we're limiting the number of posts 
# that can appear on the front page, if there are more than six Django will automatically add page navigation.

# POST DETAIL VIEW
# import View from django.views. 
# import get_object_or_404 function from Django shortcuts.

# The "PostDetail" class inherits from the View. This time we're not using one  
# of Django's helpful generic views, so we have to do everything ourselves.

# GET Method
# To display our post, we use the GET request method to get our blog post and display it. 
# we pass in self, request, slug, and *args, **kwargs (the standard other arguments and keyword arguments) as parameters. 
# Note that request must come immediately after self or the page will return an error

# Then we need to get our post object and in the list of parameters in our get method, we 
# identify slug as the post we want to display because slug is unique for each blog post:
# 1. we filter all our posts so that we only have the active ones with status set to 1. 
# 2.  we get our published post with the correct slug by passing in our queryset to 
# get_object_or_404, and then with the arguments "slug = slug".

# Now the post object contains most of the helpful things that we're looking for. 
# So using this we can get any comments that are attached to the post. 

# we're able to get the comments from our post, and we filter them to view 
# only those that are approved, we order them in ascending order so that we have the  
# oldest comment first and we can actually view  this as a conversation.
# and then store them in a comment variable.
# we set a boolean value to say whether our logged-in user had liked this post or not. 
# so, we'll set the boolean to true, otherwise it  will remain false.
# we check with an if statement to see if our post, when we filter it out 
# if the user id is actually there to say that they've liked the post. 
# If they are, we'll set it to true, otherwise it will remain false.

# Finally, for this view, we send all this information to our render method.  
# So we return render, send a request through, supply the template that we require, "post_detail.html".
# Then we create a dictionary here to supply our context. So our post will be simply post, 
# our comments key will be the comments that we got back, and liked will be our liked boolean.

# # we import the form and render it as part of our view, simply add it to our context.
# So just under liked in our render method, we're going to supply a new key comment_form, 
# and the value will just be the comment  form that we imported just now.
# We then go to our "post_detail" template to get the form displaying. 
# 
# POST Method
# this will get all of the data  that we posted from our form.
# Now our form has a method called is  valid that returns a Boolean value regarding 
# whether the form is valid, as in  all the fields have been completed or not. 
# If it is valid, a comment has been left and we want to process it. 
# And what we're going to do is set our email and our username automatically from the logged in user.
# This is conveniently passed in as part of the request so that we can  get those details from there.
# So we set the email to the request.user email. We set the instance name  to the request username.
# And then, we're going to call  the save method on our form but we're not actually going to  commit it to the database 
# yet. The reason is that we want to first assign a post to it. So comment.post equals our post instance,  
# so that we know which post a comment has  been left on and then we can save it. 
# We add an else clause as well because if the form is not valid, we want to return an empty comment form instance. 

# In the render method, set commented value to True, which has a corresponding False value  to our get 
# method. We're doing this so that we can tell our user that their comment is awaiting approval,  
# Note that we use this Boolean condition in our "post_detail" template.
# And what we're doing is saying that if our commented boolean value is set to True, that is, if 
# if commented, then instead  of the comments form, we'll display a message saying, your comment 
# is awaiting approval. Otherwise, if it's set to False, we'll display the comment form.

# POSTLIKE view
# If we haven't already liked the  post, then we need to mark it as liked. 
# If we have, then we need to mark it as unliked. In effect, we're toggling the state.
# So first, let's get the relevant  post using our get_object_or_404 method. Then, we'll toggle the state.
# We use an if statement to check if our post is already liked and if it is we'll remove the like.
# So remember how we checked if a  post was already liked before?
# We used an if statement, we filtered our post.likes on the user ID and if 
# the user ID exists, then it's been liked, so we can remove it.
# If it hasn't already been liked, then we need to add the like.  

# Now we need to reload our post_detail  template so that we can see the results.
# To do this, we'll use a new response type called HttpResponseRedirect, which we import from django.http on top of our views.py file 
# And we also need to add the reverse shortcut. This allows us to look up a URL by the name that we give it in our urls.py file. 
# And the arguments will be the slugs, so that we know which post to load. So now when we like or unlike a post it will reload our page.