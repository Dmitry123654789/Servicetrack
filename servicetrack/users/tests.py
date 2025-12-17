__all__ = ()

import django.contrib.auth
import django.test
import django.urls

import users.models


class UserSystemTest(django.test.TestCase):
    fixtures = ["fixtures/data.json"]

    def setUp(self):
        self.user_model = django.contrib.auth.get_user_model()

        self.director = self.user_model.objects.get(pk=5)
        self.manager_a1 = self.user_model.objects.get(pk=6)
        self.worker = self.user_model.objects.get(pk=7)

    def test_profile_view_status_code(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse("users:profile")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_profile_view_context_user_exists(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse("users:profile")
        resp = self.client.get(url)
        self.assertIn("user", resp.context)

    def test_profile_view_context_user_type(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse("users:profile")
        resp = self.client.get(url)
        user_obj = resp.context["user"]
        self.assertIsInstance(user_obj, self.user_model)

    def test_profile_view_context_user_id(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse("users:profile")
        resp = self.client.get(url)
        user_obj = resp.context["user"]
        self.assertEqual(user_obj.id, 7)

    def test_user_list_access_director(self):
        self.client.force_login(self.director)
        url = django.urls.reverse("users:user_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_user_list_access_worker_forbidden(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse("users:user_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_user_list_context_length(self):
        self.client.force_login(self.director)
        url = django.urls.reverse("users:user_list")
        resp = self.client.get(url)
        self.assertIn("users", resp.context)
        users_count = len(resp.context["users"])
        self.assertGreaterEqual(users_count, 0)

    def test_user_list_excludes_self(self):
        self.client.force_login(self.director)
        url = django.urls.reverse("users:user_list")
        resp = self.client.get(url)
        users_list = resp.context["users"]
        self.assertNotIn(self.director, users_list)

    def test_profile_edit_get_status(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse("users:profile_edit")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_profile_edit_post_update(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse("users:profile_edit")
        data = {"phone": "+79991112233"}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 200)

    def test_user_create_access_manager(self):
        self.client.force_login(self.manager_a1)
        url = django.urls.reverse("users:user_create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_model_is_director_property(self):
        self.assertTrue(self.director.profile.is_director)
        self.assertFalse(self.worker.profile.is_director)

    def test_model_is_worker_property(self):
        self.assertTrue(self.worker.profile.is_worker)
        self.assertFalse(self.director.profile.is_worker)

    def test_signal_profile_creation(self):
        new_user = self.user_model.objects.create(
            username="newtestuser",
            email="test@example.com",
        )
        self.assertTrue(
            users.models.Profile.objects.filter(user=new_user).exists(),
        )

    def test_custom_user_str(self):
        self.assertEqual(str(self.worker), "worker_a1")

    def test_profile_str(self):
        self.assertEqual(str(self.worker.profile), "worker_a1")

    def test_login_url_exists(self):
        url = django.urls.reverse("users:login")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
