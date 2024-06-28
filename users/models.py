from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)





class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
class Package(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.customer.user.username} - {self.package.name}"