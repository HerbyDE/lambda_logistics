from django.db import models
from django.contrib.auth.models import User
from corelogistics.models import Office


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=30, blank=True)
    location = models.ForeignKey(Office, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.last_name


class Partner(models.Model):
    name = models.CharField(max_length=100, blank=False)
    location = models.ForeignKey(Office, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class External(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Partner, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.last_name
