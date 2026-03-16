from django.urls import path
from . import views
from .forms import CommentForm


app_name = 'blog'

urlpatterns = [

    # List all posts
    path('', views.post_list, name='post_list'),

    # Post detail by ID
    path('<int:id>/', views.post_detail, name='post_detail'),

    # Post detail by date + slug
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail_by_datewithslug,
        name='post_detail_by_datewithslug',
    ),

    # Share post via email
    path(
        '<int:post_id>/share/',
        views.post_share,
        name='post_share',
    ),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment')
]