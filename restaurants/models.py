from django.db import models

# Create your models here.
class Restaurant(models.Model):
    """
    Represnts a physical restaurant location.
    Even if you only support ONE restaurant today,
    this model prevents painful refactors later.
    """
    
    # Human-readable restaurant name 
    name = models.CharField(max_length=255)

    # Soft switch to disable a restaurant without deleting data 
    is_active = models.BooleanField(default=True)

    # Automatically set when the record is created 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Used in Django admin and debugging 
        return self.name