from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # List view (with optional tag filtering)
    # path('',views.PostListView.as_view(),name='post_list'),
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    # Detail views (KEEP ONLY ONE STYLE — I recommend slug-based)
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail_by_datewithslug,
         name='post_detail_by_datewithslug'),

    # Optional: keep this ONLY if you actually use ID-based URLs
    path('<int:id>/', views.post_detail, name='post_detail'),

    # Actions
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),

    path('create/', views.post_create, name='post_create'),
]