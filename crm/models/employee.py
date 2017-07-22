from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
