from django.contrib.sitemaps import Sitemap
from blog.models import Post

class PostSitemap(Sitemap):
    changefreq='weekly' 
    # site will be updated weekly
    priority=0.9
    # 1.0 is the most priority and 0.0 is the least priority

    def items(self):
        return Post.published.all()
    
    def lastmod(self,obj):
        return obj.updated #returns the post with the last updated times