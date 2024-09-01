from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    temporary_field = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    