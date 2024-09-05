from django.db import models



class ToDo(models.Model):
    title = models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title



class Notes(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.title


class Homework(models.Model):
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=600)
    due = models.DateField()
    is_finished = models.BooleanField(default=False)


    def __str__(self):
        return self.subject
    


