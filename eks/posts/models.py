from functools import cached_property
from django.db import models
from django.urls import reverse_lazy


class Post(models.Model):
    body = models.TextField()

    @cached_property
    def edit_url(self):
        return reverse_lazy("edit-post", kwargs={"pk": self.pk})
