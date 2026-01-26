from django.views import generic
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm


class PostListView(generic.ListView):
    """Optimized list view with query optimization"""
    queryset = Post.published.select_related('author').order_by('-created')
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'


class PostDetailView(generic.DetailView):
    """Optimized detail view with query optimization"""
    model = Post
    template_name = 'blog/post_detail.html'
    queryset = Post.objects.select_related('author').prefetch_related('comments')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # Only get active comments, already prefetched
        context['comments'] = [c for c in post.comments.all() if c.active]
        context['comment_form'] = CommentForm()
        return context


@require_http_methods(["GET", "POST"])
def post_detail(request, slug):
    """Optimized post detail view with comment handling"""
    post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related('comments'),
        slug=slug
    )
    comments = post.comments.filter(active=True)
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Note: Comment model doesn't have an author field, only name/email
            # If user is authenticated, we could store username in name field
            if request.user.is_authenticated:
                new_comment.name = request.user.get_full_name() or request.user.username
                new_comment.email = request.user.email or new_comment.email
            # Save the comment to the database
            new_comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting moderation.')
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })
