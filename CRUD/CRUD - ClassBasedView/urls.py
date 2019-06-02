from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from django.conf import settings
from django.conf.urls.static import static


app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('blog/create/', PostCreateView.as_view(),
         name='blog_create'),
    path('blog/<slug:title_slug>/', PostDetailView.as_view(), name='blog_detail'),
    path('blog/<slug:title_slug>/update/',
         PostUpdateView.as_view(), name='blog_update'),
    path('blog/<slug:title_slug>/delete/',
         PostDeleteView.as_view(), name='blog_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
