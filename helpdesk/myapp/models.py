from django.db import models
from django.contrib.auth.models import User

class userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

class taskdetails(models.Model):
    STATUS = [
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("closed", "Closed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tasks"
    )
    assigned_to = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_tasks"
    )
    closed_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="closed_tasks"
    )

    task_status = models.CharField(max_length=20, choices=STATUS, default="new")
    created_on = models.DateTimeField(auto_now_add=True)

    due_date = models.DateField(null=True, blank=True)
    reward = models.IntegerField(default=0)

    # ✅ NEW FIELD
    excel_file = models.FileField(
        upload_to="task_excels/",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title



#mycart model
class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(taskdetails, on_delete=models.CASCADE)
    task_count= models.IntegerField(default=1)

class Task(models.Model):
    title = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    