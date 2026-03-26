from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from .forms import PostForm


def post_list(request, tag_slug=None):
    all_posts = Post.objects.all()
    tag = None

    if tag_slug:
        try:
            # FIXED: Use tag_slug and case-insensitive lookup
            tag = get_object_or_404(Tag, slug__iexact=tag_slug)
        except Tag.DoesNotExist:
            raise Http404("No Tag Found")
        all_posts = all_posts.filter(tags__in=[tag])

    paginator = Paginator(all_posts, 3)

    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # FIXED: use string key 'tag' in context
    return render(request, 'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag})


def post_detail(request, id):
    try:
        post = get_object_or_404(Post, id=id)
    except Post.DoesNotExist:
        raise Http404("No Post Found")

    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )


def post_detail_by_datewithslug(request, year, month, day, post):
    # This will raise 404 automatically if not found
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    # Form for users to comment
    form = CommentForm()

    # List of similar posts
    post_tags_id = post.tags.values_list("id", flat=True)
    similar_posts = Post.objects.filter(
        tags__in=post_tags_id
    ).exclude(id=post.id).annotate(
        same_tags=Count('tags')
    ).order_by("-same_tags", "-publish")[:4]

    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts
        }
    )


def post_share(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
    except Post.DoesNotExist:
        raise Http404("No Post Found")

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} ({cd['email']}) recommends you read {post.title}"

            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"

            send_mail(
                subject,
                message,
                'your_email@example.com',
                [cd['to']],
                fail_silently=False
            )

            sent = True

    else:
        form = EmailPostForm()

    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )


@require_POST
def post_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("No Page Found")

    comment = None

    # A comment was posted
    form = CommentForm(data=request.POST)

    if form.is_valid():
        # create a comment object
        comment = form.save(commit=False)

        # Assign the post to the comment
        comment.post = post

        # save the comment in the database
        comment.save()

        return render(
            request,
            'blog/post/comment.html',
            {
                'post': post,
                'form': form,
                'comment': comment
            }
        )
    else:
        # if form is invalid, still show the post with errors
        return render(
            request,
            'blog/post/comment.html',
            {
                'post': post,
                'form': form,
                'comment': comment
            }
        )

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user   # important
            post.save()
            form.save_m2m()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()

    return render(request, 'blog/post/add_post.html', {'form': form})