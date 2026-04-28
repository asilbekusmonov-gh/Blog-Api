from django.db.models import Model, ForeignKey, CASCADE, ManyToManyField
from django.db.models.fields import CharField, TextField, DateTimeField, PositiveIntegerField, BooleanField


class Category(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(Model):
    title = CharField(max_length=100)
    content = TextField()
    author = ForeignKey("apps.User", CASCADE, related_name="posts")
    created_at = DateTimeField(auto_now_add=True)
    is_published = BooleanField(default=False)
    views_count = PositiveIntegerField(default=0)
    category = ForeignKey("apps.Category", on_delete=CASCADE, related_name="posts")
    tags = ManyToManyField("apps.Tag", related_name="posts")


class Tag(Model):
    name = CharField(max_length=100)


class Like(Model):
    user = ForeignKey("apps.User", on_delete=CASCADE, related_name="likes")
    post = ForeignKey("Post", on_delete=CASCADE, related_name="likes")

    class Meta:
        unique_together = (("user", "post"),)
