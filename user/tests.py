from django.test import TestCase
from user.forms import LoginForm, RegisterForm
from user.models import User
from django.contrib import auth

test_email = "test@email.com"
required_err_msg = "This field is required."


class TestRegisterationForm(TestCase):
    def test_registeration_form_confirm_password_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields["confirm_password"].label == "Confirm Password")

    def test_registeration_form_unique_email_validation(self):
        User.objects.create(email="testemail@email.com", password="test_password")
        user_data = {
            "email": "testemail@email.com",
            "password": "123456",
            "confirm_password": "123456",
        }
        form = RegisterForm(user_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"][0], "email is taken")

    def test_registeration_form_password_match_validation(self):
        user_data = {
            "email": test_email,
            "password": "123456",
            "confirm_password": "54621",
        }
        form = RegisterForm(user_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["confirm_password"][0], "Your passwords must match"
        )

    def test_registeration_form_validates_user(self):
        user_data = {
            "email": test_email,
            "password": "123456",
            "confirm_password": "123456",
        }
        form = RegisterForm(user_data)
        self.assertTrue(form.is_valid())

    def test_registeration_form_required_fields(self):
        form = RegisterForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"][0], required_err_msg)
        self.assertEqual(form.errors["password"][0], required_err_msg)


class TestLoginForm(TestCase):
    def test_login_form_required_fields(self):
        form = LoginForm({})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors["email"][0], required_err_msg)
        self.assertEqual(form.errors["password"][0], required_err_msg)


class AuthTestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create_user("test@dom.com", "pass")
        self.u.staff = True
        self.u.superuser = True
        self.u.active = True
        self.u.save()

    def testLogin(self):
        self.client.login(username="test@dom.com", password="pass")
