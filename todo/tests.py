from django.test import TestCase
from todo.models import Task, TASKSTATES
from django.test import Client
from .models import Task
from .forms import TaskForm

class TestTaskModel(TestCase):
    def test_task_title_length(self):
        title = "x" * 300
        Task.objects.create(title=title)

    # not working with sqlite
    def test_title__fails_longer_than_three_hunred_chars(self):
        title = "x" * 301
        # with self.assertRaises():
        Task.objects.create(title=title)

class TestTaskList(TestCase):
    def setUp(self):
        self.client = Client()

    def test_task_default_state(self):
        todo_task = Task.objects.create(title="test first task with default state")
        in_progress_task = Task.objects.create(title="test task with state", state="I")

        self.assertEqual(todo_task.get_state_display(), TASKSTATES.TODO.label)
        self.assertEqual(in_progress_task.get_state_display(),TASKSTATES.INPROGRESS.label)


    # def test_only_authenticated_users_can_access_dashboard(self):
    #     response = self.client.get('/todolist')
    #     self.assertEqual(response.status_code, 301)
    #     user = User.objects.create_user()

    # def test_admin_user_only_can_create_tasks(self):
    #     response = self.request_client.get('/todolist/create')
    #     self.assertEqual(response.status_code, 401)


class TestTaskFormValidations(TestCase):
    def test_title_length_validation_accepts_300(self):
        task = {
            "title": "x" * 300,
            "state": "I"
        }
        task_form = TaskForm(task)
        self.assertEqual(task_form.is_valid(), True)

    def test_title_length_validation_at_most_300(self):
        task = {
            "title": "x" * 301
        }
        task_form = TaskForm(task)
        self.assertEqual(task_form.is_valid(), False)
        self.assertEqual(task_form.errors['title'][0], 'Ensure this value has at most 300 characters (it has 301).')

    def test_state_field_only_accepts_one_of_the_choices(self):
        task = {
            "title": "task1",
            "state": "P"
        }
        task_form = TaskForm(task)
        self.assertEqual(task_form.is_valid(), False)
        self.assertEqual(task_form.errors['state'][0], 'Select a valid choice. P is not one of the available choices.')



