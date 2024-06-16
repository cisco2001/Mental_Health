from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, AbstractBaseUser, Group, Permission
from django.db import models
from django.conf import settings



class Student(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    birth_date = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    university = models.CharField(max_length=100)

    groups = models.ManyToManyField(Group, related_name='student_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='student_permissions_set', blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class StaffManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class Staff(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(Group, related_name='staff_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='staff_permissions_set', blank=True)
    
    objects = StaffManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

class Appointment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_appointments')
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, related_name='staff_appointments')
    date = models.DateField()
    text = models.TextField(blank=True, null=True)
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.staff} on {self.date}"