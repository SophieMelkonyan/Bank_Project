from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password, first_name, last_name,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user =self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email,password,first_name,last_name,**extra_fields):
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        return self._create_user(email,password,first_name,last_name,**extra_fields)

    def create_superuser(self,email,password,first_name,last_name,**extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        return self._create_user(email,password,first_name,last_name,**extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,max_length=40)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    data=models.DateField(auto_now_add=True)
    bank_account=models.IntegerField(default=0)
    card_account = models.IntegerField(default=0)
    balance=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    pin_code = models.IntegerField(default=0)
    bank = models.CharField(max_length=40,default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['first_name','last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
