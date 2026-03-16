from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST


def post_list(request):
    all_posts = Post.objects.all()
    paginator = Paginator(all_posts, 3)

    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)

    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )


def post_detail_by_datewithslug(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
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
        post = post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("No Page Found")
    comment=None
    #A comment was posted
    form=CommentForm(data=require_POST)
    if form.is_valid():
        #create a comment object
        comment=form.save(commit=False)
        #Assign the post to the comment
        comment.post=post
        #save the comment in the database
        comment.save()
        return render(
            request,
            'blog/post/comment.html',
            {
                'post':post,
                'form':form,
                'comment':comment
            }
        )