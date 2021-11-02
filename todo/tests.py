from django.test import TestCase
from rest_framework.test import APIClient
from todo.models import Task,TASKSTATES
from django.test import Client

class TestTaskList(TestCase):
    def setUp(self):
        Task.objects.create(title="test first task with default state")
        Task.objects.create(title="test task with state", state="I")
        self.request_client = APIClient()
        self.client = Client()

    def test_task_default_state(self):
        todo_task = Task.objects.get(title="test first task with default state")
        in_progress_task = Task.objects.get(title="test task with state")
        self.assertEqual(todo_task.get_state_display(), TASKSTATES.TODO.label)
        self.assertEqual(in_progress_task.get_state_display(),TASKSTATES.INPROGRESS.label)

    # def test_only_authenticated_users_can_access_dashboard(self):
    #     response = self.client.get('/todolist')
    #     self.assertEqual(response.status_code, 301)
    #     user = User.objects.create_user()

    # def test_admin_user_only_can_create_tasks(self):
    #     response = self.request_client.get('/todolist/create')
    #     self.assertEqual(response.status_code, 401)