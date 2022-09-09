from django.views import generic
from .models import Post
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404

# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active= True)
    new_comment = None


    #Comment Posted
   
    if request.method == 'POST':
        comment_form = CommentForm(data = request.POST)

        if comment_form.is_valid():
            #create the comment object but don't store it to database yet
            new_comment = comment_form.save(commit=False)

            #Assign the current post to comment
            new_comment.post = post

            #Save to Database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post':post,
                                            'comments': comments,
                                            'new_comment': new_comment,
                                            'comment_form': comment_form})
