from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel


class AbstractEmployee(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    manager = models.BooleanField(default=False)
    status = models.ForeignKey(
        'employee.Status', 
        on_delete=models.CASCADE, 
        null=True
    )
    position = models.ForeignKey(
        'employee.Position', 
        on_delete=models.CASCADE, 
        null=True
    )
    department = models.ForeignKey(
        'employee.Department', 
        on_delete=models.CASCADE, 
        null=True
    )
    image = models.ImageField(
        upload_to='employee/images/', 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True

class AbstractStatus(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True

class AbstractPosition(BaseModel):
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
    
class AbstractDepartment(BaseModel):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(
        'employee.Employee', 
        on_delete=models.CASCADE, 
        null=True, 
        related_name='departments'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True

