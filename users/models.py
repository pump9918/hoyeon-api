from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractUser, UserManager

class User(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128)
    email = models.EmailField(db_index=True, unique=True)
    gender = models.CharField(
        choices=(
            ('F', 'female'),
            ('M', 'male')
        ), max_length=1, blank=True)
    birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=128, blank=True)

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=10, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.user.email