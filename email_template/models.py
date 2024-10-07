from django.db import models
from datetime import datetime, date


class TemplateModel(models.Model):
    name = models.TextField(max_length=100)
    subject = models.TextField(max_length=255)
    body = models.TextField()
    file = models.FileField(upload_to="resumes/", default=None)

    class Meta:
        db_table = 'templatemodel'

    def __str__(self):
        return self.name
    

class EmailModel(models.Model):
    template = models.TextField(max_length=100)
    to = models.TextField(max_length = 255)
    name = models.TextField(max_length = 50)
    date = models.DateField(default = date.today())
    time = models.TimeField(default = datetime.now())

    class Meta:
        db_table = 'emailmodel'

    def __str__(self):
        return self.name