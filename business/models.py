import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class UserProfile(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

class Article(models.Model):
    class PublicStatus(models.TextChoices):
        PUBLIC = "Público", "Público"
        PRIVATE = "Privado", "Privado"
        REVISION = "Em Revisão", "Em Revisão"
        
    title = models.CharField(max_length=1000)
    description = models.TextField()
    tags = models.CharField()
    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    public_since = models.DateTimeField(null=True, blank=True)
    public = models.CharField(max_length=15, choices=PublicStatus.choices, default=PublicStatus.REVISION)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="article", null=False)
    mainImage = models.ImageField(upload_to="", null=True, blank=True)
    slug  = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
