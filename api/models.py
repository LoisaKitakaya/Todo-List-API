from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TodoList(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_owner')
    thing_to_do = models.CharField(max_length=250, blank=True)
    completed = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True, blank=True)

    class Meta:

        ordering = ['-created_on']

    def __str__(self):

        return self.thing_to_do
