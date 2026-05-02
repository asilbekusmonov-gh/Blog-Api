from io import BytesIO

from PIL import Image
from django.db.models import Exists, OuterRef, Value, BooleanField
from django.db.models.aggregates import Count
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import Product, Favorite, Course, Enrollment, Post, Book
from apps.serializers import PostModelSerializer, BookModelSerializer


# from apps.serializers import ProductModelSerializer, CourseModelSerializer


# from apps.filters import PostFilter
# from apps.models import Post, Like
# from apps.permissions import PostPermission
# # from apps.serializers import PostModelSerializer


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')
    serializer_class = PostModelSerializer
    pagination_class = None

    def get(self, request):
        pass


    # http_method_names = ['get', 'post']
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filterset_class = PostFilter
    # ordering_fields = 'created_at', 'views_count', 'likes_count'
    # search_fields = 'title', 'content'
    # base_permissions = [IsAuthenticated, PostPermission]
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


# class CourseModelViewSet(ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseModelSerializer
#
#     @action(detail=True, methods=["get"])
#     def enroll(self, request, pk=None):
#         Enrollment.objects.get_or_create(user=request.user, course_id=pk)
#
#         return Response({"enrolled": True})
#
#     @action(detail=True, methods=["delete"])
#     def unenroll(self, request, pk=None):
#         Enrollment.objects.filter(course_id=pk, user=request.user).delete()
#         return Response({"enrolled": False})


# from django.contrib.contenttypes.models import ContentType
# from rest_framework.views import APIView
#
#
# class LikeToggleView(APIView):
#
#     def post(self, request, model_name, object_id):
#
#         model_map = {
#             'post': Post,
#             'product': Product,
#             'course': Course,
#         }
#
#         model_class = model_map.get(model_name)
#         if not model_class:
#             return Response({'error': 'Notogri model nomi'}, status=400)
#
#         ct = ContentType.objects.get_for_model(model_class)
#
#         like, created = Like.objects.get_or_create(
#             user=request.user,
#             content_type=ct,
#             object_id=object_id
#         )
#
#         if not created:
#             like.delete()
#             return Response({'status': 'unlike qilindi '})
#
#         return Response({'status': 'like qilindi '})


class BookModelViewSet(ModelViewSet):
    queryset = Book.objects.annotate_with_availability()
    serializer_class = BookModelSerializer

    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = ['title', 'author__username']
    ordering_fields = ['rating', 'published_year', 'available_copies']




class BookThumbnailView(APIView):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        img = Image.open(book.image.path)

        img.thumbnail((150, 150))

        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)

        return FileResponse(buffer, content_type="image/jpeg")