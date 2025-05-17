from django.db import models

class UserProfile(models.Model):
    category = models.CharField(max_length=20, default='DELEGATE')
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    regno = models.CharField("REGNO", max_length=50, null=True, blank=True)
    qrcode = models.CharField("QRCODE", max_length=200, null=True, blank=True)
    print_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.company})"