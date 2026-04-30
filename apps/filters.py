from django_filters import FilterSet, DateTimeFilter, NumberFilter

from apps.models import Post

# class PostFilter(FilterSet):
#     from_time = DateTimeFilter(field_name='created_at', lookup_expr='gte')
#     to_time = DateTimeFilter(field_name='created_at', lookup_expr='lte')
#     views_count = NumberFilter(field_name='views_count', lookup_expr='gte')
#     likes_count = NumberFilter(field_name='likes_count', lookup_expr='gte')
#
#     class Meta:
#         model = Post
#         fields = 'category', 'tags',
