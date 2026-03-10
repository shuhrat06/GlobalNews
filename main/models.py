from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length = 300, null=True, blank=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    slug = models.SlugField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            unique_slug = slug
            count = 1
            qs = Category.objects.all()

            if self.id:
                qs = qs.exclude(id=self.id)

            while qs.filter(slug = unique_slug).exists():
                unique_slug = f"{slug}-{count}"
                count+=1
            self.slug = unique_slug

        return super().save(*args, **kwargs)
    
class Article(models.Model):
    title = models.CharField(max_length=255)
    intro = models.TextField()
    cover = models.ImageField(upload_to='articles')
    author = models.CharField(max_length=32, blank=True, null=True)
    read_time = models.DurationField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    slug = models.SlugField(unique=True, default="", max_length=300)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:

            slug = slugify(self.title)
            unique_slug = slug
            count = 1
            qs = Article.objects.all()

            if self.id:
                qs = qs.exclude(id=self.id)

            while qs.filter(slug = unique_slug).exists():
                unique_slug = f"{slug}-{count}"
                count+=1
            self.slug = unique_slug
        return super().save(*args, **kwargs)

class Content(models.Model):
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='contents/',null=True,blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"Content of {self.article.title}"



class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}: {self.text}"
    


class Moment(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='moments/')
    author = models.CharField(max_length=32, blank=True, null=True)
    published = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.subject}"


class Newsletter(models.Model):
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}'


