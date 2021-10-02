from django.db import models
from django.db.models.base import Model
class Task(models.Model):
    TODO = 'T'
    INPROGESSS = 'I'
    DONE = 'D'
    TASK_STATES = (
        (TODO, 'To-DO'),
        (INPROGESSS, 'In-progress'),
        (DONE, 'Done'),
    )

    title=models.CharField(max_length=300)
    state=models.CharField(max_length=200,choices=TASK_STATES, default=TODO)
    creation_date=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title