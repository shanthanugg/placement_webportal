from django.db import models

# Create your models here.


from django.db import models

class Student(models.Model):
    # Define your student model fields here
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    # Define other fields as needed

    def __str__(self):
        return self.name
