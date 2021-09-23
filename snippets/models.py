from django.db import models

from wagtail.snippets.models import register_snippet


@register_snippet
class Author(models.Model):
  
    author_name = models.CharField(max_length=50, blank=False, null=False)
    biography = models.TextField(max_length=500, blank=False, null=False)

    def __str__(self):
        """The string representation of this class"""

        return f"{self.author_name}"

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
