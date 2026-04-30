from django.db.models import Exists, OuterRef, Value, BooleanField
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.models import Product, Favorite, Course, Enrollment
from apps.serializers import CourseModelSerializer


# from apps.serializers import ProductModelSerializer, CourseModelSerializer


# from apps.filters import PostFilter
# from apps.models import Post, Like
# from apps.permissions import PostPermission
# # from apps.serializers import PostModelSerializer


# class PostModelViewSet(ModelViewSet):
#     queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')
#     serializer_class = PostModelSerializer
#     http_method_names = ['get', 'post']
#     filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
#     filterset_class = PostFilter
#     ordering_fields = 'created_at', 'views_count', 'likes_count'
#     search_fields = 'title', 'content'
#     base_permissions = [IsAuthenticated, PostPermission]
#
#     @action(detail=True, methods=['post'], url_path='likes', serializer_class=None)
#     def set_likes(self, request, pk=None):
#         Like.objects.get_or_create(user=request.user, post_id=pk)
#         return Response({'status': 'success'})
#
#     @action(detail=True, methods=['delete'], url_path='unlikes', serializer_class=None)
#     def set_unlikes(self, request, pk=None):
#         Like.objects.filter(user=request.user, post_id=pk).delete()
#         return Response({'status': 'success'})
#
#     @action(detail=False, methods=['get'], serializer_class=None)
#     def popular(self, request):
#         qs = self.get_queryset().order_by('-views_count')
#         serializer = PostModelSerializer(qs, many=True)
#         return Response(serializer.data)
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#
#         return qs.annotate(likes_count=Count('likes'))

# @action(detail=False, methods=['get'])
# def my_posts(self, request):
#     posts = Post.objects.filter(author=request.user)
#     serializer = self.get_serializer(posts, many=True)
#     return Response(serializer.data)


# class ProductViewSet(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductModelSerializer
#     base_permissions = []
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         user = self.request.user
#
#         if user.is_authenticated:
#             key = Exists(Favorite.objects.filter(product_id=OuterRef('pk'), user=user))
#         else:
#             key = Value(False, BooleanField())
#         return qs.annotate(favorites_count=Count('favorites'), is_favorited=key)




class CourseModelViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer

    @action(detail=True, methods=["get"])
    def enroll(self, request, pk=None):
        Enrollment.objects.get_or_create(user=request.user, course_id=pk)

        return Response({"enrolled": True})

    @action(detail=True, methods=["delete"])
    def unenroll(self, request, pk=None):
        Enrollment.objects.filter(course_id=pk, user=request.user).delete()
        return Response({"enrolled": False})


