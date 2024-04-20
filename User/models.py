from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import random


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=40)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, default="")
    bank_account = models.IntegerField(default=0)
    card_account = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pin_code = models.IntegerField(default=0)
    bank = models.CharField(max_length=40, default="")

    def save(self, *args, **kwargs):
        if not self.bank_account:
            self.bank_account = int(''.join(str(random.randint(0, 9)) for _ in range(14)))
        if not self.card_account:
            self.card_account = int(''.join(str(random.randint(0, 9)) for _ in range(12)))
        super().save(*args, **kwargs)



    def is_luhn_valid(self, card_number):
        return self.luhn_checksum(card_number) == 0


    def generate_card_number(self):
        while True:
            card_number = random.randint(10 ** 14, (10 ** 16) - 1)
            if self.is_luhn_valid(card_number):
                return card_number

    def luhn_checksum(self, card_number):
        card_digits = [int(digit) for digit in str(card_number)]
        for i in range(len(card_digits) - 2, -1, -2):
            card_digits[i] *= 2
            if card_digits[i] > 9:
                card_digits[i] -= 9
        checksum = sum(card_digits) % 10
        return checksum
