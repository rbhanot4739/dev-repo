from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return f"/posts/detail/{self.id}"
        return reverse("post-detail", kwargs={'id': self.id})
