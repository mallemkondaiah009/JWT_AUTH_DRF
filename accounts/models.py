from django.db import models

class User(models.Model):
    username = models.CharField(max_length=12,unique=True,db_index=True)
    email = models.EmailField(max_length=20,unique=True,db_index=True)
    password = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
