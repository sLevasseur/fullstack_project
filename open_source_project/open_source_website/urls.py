
from django.urls import path
from .views import Homepage, Blogs, One_blog, Unsubscribe, Legal_Stuff

urlpatterns = [
    path('', Homepage.as_view(), name="index"),
    path('blog/', Blogs.as_view(), name="blog"),
    path('blog/<int:pk>/', One_blog.as_view(), name="one_blog"),
    path('unsubscribe/', Unsubscribe.as_view(), name="unsubscribe"),
    path('legal_stuff/', Legal_Stuff.as_view(), name="legal_stuff")

]


