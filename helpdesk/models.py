from django.db import models
import uuid

# Create your models here.


def gen_ticket_no():
    return uuid.uuid4().hex[:6].upper()


class InternalEnquiry(models.Model):
    ticket_no = models.CharField(max_length=6, blank=False, unique=True, default=gen_ticket_no)
    title = models.CharField(max_length=100, blank=False)
    user_detail = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    technical_issue = models.CharField(max_length=300, blank=True)
    message = models.TextField(blank=False)

    def __str__(self):
        return self.ticket_no


class ExternalEnquiry(models.Model):
    ticket_no = models.CharField(max_length=6, blank=False, unique=True, default=gen_ticket_no)
    title = models.CharField(max_length=100, blank=False)
    name_surname = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False)
    phone = models.CharField(blank=True, max_length=50)
    technical_issue = models.CharField(max_length=300, blank=True)
    message = models.TextField(blank=False)

    def __str__(self):
        return self.ticket_no


class WikiEntry(models.Model):
    title = models.CharField(max_length=50, blank=False)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=False)
    excerpt = models.TextField(blank=False)
    body = models.TextField(blank=False)
    image = models.ImageField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    title = models.CharField(max_length=50, blank=False)
    author = models.CharField(max_length=100, blank=False)
    body = models.TextField(blank=False)

    def __str__(self):
        return self.title

class FAQ(models.Model):
    title = models.CharField(max_length=200, blank=False)
    internal = models.BooleanField(default=True, blank=False)
    body = models.TextField()

    def __str__(self):
        return self.title

class HelpDeskGuideLine(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title