from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User
from room.models import Room, Language


class UserLoginViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@mail.com')
        user.set_password('thisistest')
        user.save()

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(id=1)

    def test_can_show_login_page(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/accounts_login.html')

    def test_can_login(self):
        logged_in = self.client.login(
            email='test@mail.com', password='thisistest')
        self.assertTrue(logged_in)

    def test_redirect_index_page_after_login(self):
        response = self.client.post(reverse('accounts:login'), {
                                    'email': 'test@mail.com', 'password': 'thisistest'}, follow=True)
        self.assertTemplateNotUsed(response, 'accounts/accounts_login.html')
        self.assertTemplateUsed(response, 'room/room_index.html')

    def test_authenticated_user_cannnot_enter_login_page(self):
        is_logged_in = self.client.login(
            email='test@mail.com', password='thisistest')
        self.assertTrue(is_logged_in)
        response = self.client.get(reverse('accounts:login'), follow=True)
        self.assertTemplateNotUsed(response, 'accounts/accounts_login.html')
        self.assertTemplateUsed(response, 'room/room_index.html')

    def test_redirect_login_page_if_email_or_password_wrong(self):
        response = self.client.post(reverse('accounts:login'), {
                                    'email': 'wrong@mail.com', 'password': 'wrong'}, follow=True)
        self.assertTemplateNotUsed(response, 'room/room_index.html')
        self.assertTemplateUsed(response, 'accounts/accounts_login.html')


class UserLogoutViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@mail.com')
        user.set_password('thisistest')
        user.save()

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(id=1)

    def test_can_logout(self):
        is_logged_in = self.client.login(
            email='test@mail.com', password='thisistest')
        self.assertTrue(is_logged_in)

    def test_redirect_to_login_page_after_logout(self):
        _ = self.client.login(email='test@mail.com', password='thisistest')
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/accounts_login.html')

    def test_unauthenticated_user_will_redirect_to_login_page(self):
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertTemplateUsed(response, 'accounts/accounts_login.html')


class UserRegisterViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@mail.com')
        user.set_password('thisistest')
        user.save()

    def setUp(self):
        self.client = Client()

    def test_can_show_user_signup_page(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/accounts_register.html')

    def test_unauthenticated_user_cannot_enter_signup_page(self):
        _ = self.client.post(reverse('accounts:signup'), {
            'username': 'newuser',
            'email': 'newuser@mail.com',
            'password': 'thisistest',
            'confirm_password': 'thisistest'})
        response = self.client.get(reverse('accounts:signup'), follow=True)
        self.assertTemplateUsed(response, 'room/room_index.html')
        self.assertTemplateNotUsed(response, 'accounts/accounts_register.html')

    def test_can_create_new_account(self):
        _ = self.client.post(reverse('accounts:signup'), {
            'username': 'newuser',
            'email': 'newuser@mail.com',
            'password': 'thisistest',
            'confirm_password': 'thisistest'})
        new_user = User.objects.get(email='newuser@mail.com')
        self.assertEqual(new_user.username, 'newuser')
        self.assertEqual(new_user.email, 'newuser@mail.com')

    def test_redirect_to_index_page_if_form_is_valid(self):
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'newuser',
            'email': 'newuser@mail.com',
            'password': 'thisistest',
            'confirm_password': 'thisistest'}, follow=True)
        self.assertTemplateUsed(response, 'room/room_index.html')

    def test_redirect_to_signup_page_if_form_is_invalid(self):
        response = self.client.post(reverse('accounts:signup'), {}, follow=True)
        self.assertTemplateUsed(response, 'accounts/accounts_register.html')

    def test_automatically_login_after_success_signup(self):
        _ = self.client.post(reverse('accounts:signup'), {
            'username': 'newuser',
            'email': 'newuser@mail.com',
            'password': 'thisistest',
            'confirm_password': 'thisistest'})
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertTemplateUsed(response, 'accounts/accounts_login.html')
    

class UserProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@mail.com')
        user.set_password('thisistest')
        user.save()

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(id=1)

    def test_can_show_user_profile_page(self):
        _ = self.client.login(
            email='test@mail.com',
            password='thisistest'
        )
        response = self.client.get(reverse('accounts:profile', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'accounts/accounts_profile.html')

    def test_unauthenticated_user_cannot_enter_user_profile_page(self):
        response = self.client.get(reverse('accounts:profile', args=[self.user.id]), follow=True)
        self.assertTemplateUsed(response, 'accounts/accounts_login.html')
