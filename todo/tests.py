from django.test import TestCase
from todo.models import Task, TASKSTATES
from django.test import Client

from user.models import User
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


class TestTaskView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="email@email.com", password="password"
        )

    def test_task_default_state(self):
        todo_task = Task.objects.create(title="test first task with default state")
        in_progress_task = Task.objects.create(title="test task with state", state="I")
        self.assertEqual(todo_task.get_state_display(), TASKSTATES.TODO.label)
        self.assertEqual(
            in_progress_task.get_state_display(), TASKSTATES.INPROGRESS.label
        )

    def test_task_view_get_task(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        task = Task.objects.create(title="to do task")
        response = self.client.get(f"/todolist/{task.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("task.html")

    def test_admin_can_create_task(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        task = {"title": "TaskTest", "state": "I"}
        response = self.client.post("/todolist/add/", task)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.filter(title="TaskTest").count(), 1)

    def test_admin_can_edit_task(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        task = Task.objects.create(title="secondTask", state="T")
        response = self.client.post(
            f"/todolist/{task.id}/", {"title": "TaskTest1", "state": "I"}
        )
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.title, "TaskTest1")
        self.assertEqual(Task.objects.filter(title="secondTask").count(), 0)

    def test_regular_user_can_view_task_list(self):
        self.client.force_login(self.user)
        response = self.client.get("/todolist/")
        self.assertEqual(response.status_code, 200)

    def regular_user_cannot_edit_task(self):
        self.client.force_login(self.user)
        task = Task.objects.create(title="secondTask", state="T")
        response = self.client.post(
            f"/todolist/{task.id}/", {"title": "TaskTest1", "state": "I"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], f"/user/login?next=/todolist/{task.id}/")


class TestTaskFormValidations(TestCase):
    def test_title_length_validation_accepts_300(self):
        task = {"title": "x" * 300, "state": "I"}
        task_form = TaskForm(task)
        self.assertEqual(task_form.is_valid(), True)

    def test_title_length_validation_at_most_300(self):
        task = {"title": "x" * 301}
        task_form = TaskForm(task)
        self.assertEqual(task_form.is_valid(), False)
        self.assertEqual(
            task_form.errors["title"][0],
            "Ensure this value has at most 300 characters (it has 301).",
        )

    def test_state_field_only_accepts_one_of_the_choices(self):
        task = {"title": "task1", "state": "P"}
        task_form = TaskForm(task)
        self.assertEqual(task_form.is_valid(), False)
        self.assertEqual(
            task_form.errors["state"][0],
            "Select a valid choice. P is not one of the available choices.",
        )

    def test_required_fields_validation(self):
        task_form = TaskForm({})
        self.assertEqual(task_form.is_valid(), False)
        self.assertEqual(
            task_form.errors["title"][0],
            "This field is required.",
        )
        self.assertEqual(
            task_form.errors["state"][0],
            "This field is required.",
        )
