from django.test import TestCase

from django.test import TestCase
from todo.models import Task

class TaskTestCase(TestCase):
    def setUp(self):
        Task.objects.create(title="test first task with default state")
        Task.objects.create(title="test task with state", state="I")

    def test_task_default_state(self):
        todo_task = Task.objects.get(title="test first task with default state")
        in_progress_task = Task.objects.get(title="test task with state")
        self.assertEqual(todo_task.get_state_display(), 'To-DO')
        self.assertEqual(in_progress_task.get_state_display(), 'In-progress')
