from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

#  all we're doing here is telling our comment form what model to use, and 
# then which fields we want displayed on our form, in this case, body. 
# The trailing comma after body is important, otherwise Python will read 
# this as a string instead of a tuple, and that will cause an error.
# Now that we've added that, we head over to our views.py file and import the form we just created.