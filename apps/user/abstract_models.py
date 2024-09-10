import uuid
from django.contrib.auth.models import AbstractUser as BaseAbstractUser
from django.db import models
from core.models import BaseModel

class AbstractUser(BaseAbstractUser, BaseModel):
    def auto_generate_id():
        return f'US{uuid.uuid4().hex.upper()}'
    
    id = models.CharField(
        primary_key=True,
        max_length=40,
        default=auto_generate_id, 
        editable=False, 
    )
    
    def __str__(self):
        return self.username
    
    class Meta:
        abstract = True