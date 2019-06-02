from django.urls import path
from .views import homepage, blog_detail, blog_create, blog_update, blog_delete
from django.conf import settings
from django.conf.urls.static import static


app_name = 'blog'
urlpatterns = [
    path('', homepage, name='home'),
    path('blog/<slug:title_slug>/', blog_detail, name='blog_detail'),
    path('blog/create/', blog_create, name='blog_create'),  # why before detail?
    path('blog/<slug:title_slug>/update/', blog_update, name='blog_update'),
    path('blog/<slug:title_slug>/delete/', blog_delete, name='blog_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
