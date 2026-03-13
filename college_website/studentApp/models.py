from django.db import models
#from .models import Department (We only need this when we define Department class after student class but if we declare it before student class no need to write it.)

# Create your models here.
class Department(models.Model):
    department_code=models.CharField(max_length=50,primary_key=True)
    dept_name=models.CharField(max_length=50)
    def __str__(self):
        return f"{self.dept_name}"

class student(models.Model):
    roll_number=models.CharField(max_length=100,primary_key=True) #If we want roll number as primary key we will set
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='studentApp_students'
    )
    
    class Meta:
        ordering=['name']  #Ascending Order on the basis of name
    def __str__(self):
        return self.name
    
