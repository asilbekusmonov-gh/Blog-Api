from drf_spectacular.utils import extend_schema
from rest_framework.fields import SerializerMethodField, DateTimeField, HiddenField, CurrentUserDefault, CharField
from rest_framework.serializers import ModelSerializer, ListSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import Post, Tag, Product, Course, Skill, Enrollment


# class PostModelSerializer(ModelSerializer):
#     created_at = DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
#     likes_count = SerializerMethodField()
#     author = HiddenField(default=CurrentUserDefault())
#     tags = ListSerializer(child=CharField(), write_only=True)
#
#     class Meta:
#         model = Post
#         fields = 'title', 'content', 'is_published', 'views_count', 'likes_count', 'created_at', 'author', 'category', 'tags'
#         read_only_fields = 'views_count',
#
#     def get_likes_count(self, obj: Post):
#         return obj.likes_count
#
#     def create(self, validated_data):
#         tags = validated_data.pop('tags')
#
#         post = Post.objects.create(**validated_data)
#         for tag_name in tags:
#             tag, created = Tag.objects.get_or_create(name=tag_name)
#             post.tags.add(tag)
#
#         return post
#
#     def update(self, instance, validated_data):
#         tags_data = validated_data.pop('tags', None)
#
#         instance = super().update(instance, validated_data)
#
#         if tags_data is not None:
#             tags = []
#             for tag_name in tags_data:
#                 tag, _ = Tag.objects.get_or_create(name=tag_name)
#                 tags.append(tag)
#
#             instance.tags.set(tags)
#
#         return instance
#
#
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         data = cls.token_class.for_user(user)
#         data.payload['role'] = user.role
#         return data


# class ProductModelSerializer(ModelSerializer):
#     category_name = CharField(
#         source='category.name',
#         read_only=True
#     )
#     favorites_count = SerializerMethodField()
#     is_favorited = SerializerMethodField()
#
#     class Meta:
#         model = Product
#         fields = 'title', 'price', 'description', 'favorites_count', 'is_favorited', 'category', 'category_name'
#
#     def get_favorites_count(self, obj: Product):
#         return obj.favorites_count
#
#     def get_is_favorited(self, obj: Product):
#         return obj.is_favorited


class CourseModelSerializer(ModelSerializer):
    is_enrolled = SerializerMethodField()
    skills = ListSerializer(child=CharField(max_length=25), write_only=True)

    class Meta:
        model = Course
        fields = 'title', 'description', 'is_enrolled', 'skills', 'students_count', 'instructor'
        read_only_fields = 'is_enrolled', 'instructor'

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        skills_name = []

        for skill_name in skills:
            obj, created = Skill.objects.get_or_create(name=skill_name)
            skills_name.append(obj)

        instance = Course.objects.create(**validated_data)
        instance.skills.set(skills_name)
        return instance

    def get_is_enrolled(self, obj: Course):
        user = self.context['request'].user

        if user.is_authenticated:
            return Enrollment.objects.filter(user=user, course=obj).exists()
        return False
