from django.test import TestCase
from user.forms import RegisterForm
from user.models import User

from user.views import signup

test_email = 'test@email.com'
class TestSignUp(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testemail@email.com', password='test_password')

    def test_registeration_form_confirm_password_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['password_2'].label == 'Confirm Password')

    def test_registeration_form_unique_email_validation(self):
        user_data = {
            'email': 'testemail@email.com',
            'password': '123456',
            'password_2': '123456'
        }
        form = RegisterForm(user_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], 'email is taken')

    def test_registeration_form_password_match(self):
        user_data = {
            'email': test_email,
            'password': '123456',
            'password_2': '54621'
        }
        form = RegisterForm(user_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password_2'][0], 'Your passwords must match')

    def test_registeration_form_validates_user(self):
        user_data = {
            'email': test_email,
            'password': '123456',
            'password_2': '123456'
        }
        form = RegisterForm(user_data)
        self.assertTrue(form.is_valid())

    def tearDown(self):
        User.objects.filter(id=self.user.id).delete()

