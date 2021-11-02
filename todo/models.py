from django.db import models
class TASKSTATES(models.TextChoices):
    TODO = 'T',('TO-DO')
    INPROGRESS = 'I',('In-Progress')
    DONE = 'D',('Done')

class Task(models.Model):

    title=models.CharField(max_length=300)
    state=models.CharField(max_length=200,choices=TASKSTATES.choices, default=TASKSTATES.TODO)
    creation_date=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title