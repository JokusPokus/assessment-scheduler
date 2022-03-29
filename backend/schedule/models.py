from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = now()
        self.modified = now()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
