from django.db import models

            
class BaseModel(models.Model):

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    class Meta:
        abstract = True
        
    def update(self, save=False, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if save:
            self.save()