__all__ = ()

import django.contrib.auth
import django.test
import django.urls

import company.models


class CompanyViewsTest(django.test.TestCase):
    fixtures = ["fixtures/data.json"]

    def setUp(self):
        self.user_model = django.contrib.auth.get_user_model()

        self.director = self.user_model.objects.get(pk=5)
        self.manager_a1 = self.user_model.objects.get(pk=6)
        self.worker = self.user_model.objects.get(pk=7)

        self.org_a = company.models.Organization.objects.get(pk=1)
        self.org_b = company.models.Organization.objects.get(pk=2)
        self.group_a1 = company.models.WorkerGroup.objects.get(pk=1)
        self.group_a2 = company.models.WorkerGroup.objects.get(pk=2)

    def test_org_detail_status_code_success(self):
        self.client.force_login(self.director)
        response = self.client.get(
            django.urls.reverse(
                "company:organization_detail",
                kwargs={"pk": self.org_a.pk},
            ),
        )
        self.assertEqual(response.status_code, 200)

    def test_org_detail_context_object_name(self):
        self.client.force_login(self.director)
        response = self.client.get(
            django.urls.reverse(
                "company:organization_detail",
                kwargs={"pk": self.org_a.pk},
            ),
        )
        self.assertIn("organization", response.context)

    def test_org_detail_context_object_type(self):
        self.client.force_login(self.director)
        response = self.client.get(
            django.urls.reverse(
                "company:organization_detail",
                kwargs={"pk": self.org_a.pk},
            ),
        )
        self.assertIsInstance(
            response.context["organization"],
            company.models.Organization,
        )

    def test_org_detail_context_object_pk(self):
        self.client.force_login(self.director)
        response = self.client.get(
            django.urls.reverse(
                "company:organization_detail",
                kwargs={"pk": self.org_a.pk},
            ),
        )
        self.assertEqual(
            response.context["organization"].pk,
            self.org_a.pk,
        )

    def test_org_detail_access_forbidden_other_org(self):
        self.client.force_login(self.director)
        url = django.urls.reverse(
            "company:organization_detail",
            kwargs={"pk": self.org_b.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_org_edit_get_status_code_success_director(self):
        self.client.force_login(self.director)
        response = self.client.get(
            django.urls.reverse(
                "company:organization_edit",
                kwargs={"pk": self.org_a.pk},
            ),
        )
        self.assertEqual(response.status_code, 200)

    def test_org_edit_get_status_code_forbidden_manager(self):
        self.client.force_login(self.manager_a1)
        response = self.client.get(
            django.urls.reverse(
                "company:organization_edit",
                kwargs={"pk": self.org_a.pk},
            ),
        )
        self.assertEqual(response.status_code, 302)

    def test_org_edit_post_update_name(self):
        self.client.force_login(self.director)
        new_name = "Organization A Updated"
        data = {"name": new_name, "description": "New Description"}
        self.client.post(
            django.urls.reverse(
                "company:organization_edit",
                kwargs={"pk": self.org_a.pk},
            ),
            data,
        )
        self.org_a.refresh_from_db()
        self.assertEqual(self.org_a.name, new_name)

    def test_group_list_status_code_success(self):
        self.client.force_login(self.worker)
        response = self.client.get(django.urls.reverse("company:group_list"))
        self.assertEqual(response.status_code, 200)

    def test_group_list_context_groups_key(self):
        self.client.force_login(self.director)
        response = self.client.get(django.urls.reverse("company:group_list"))
        self.assertIn("groups", response.context)

    def test_group_list_queryset_size_for_org_a(self):
        self.client.force_login(self.director)
        response = self.client.get(django.urls.reverse("company:group_list"))
        self.assertEqual(len(response.context["groups"]), 2)

    def test_group_detail_status_code_success(self):
        self.client.force_login(self.worker)
        response = self.client.get(
            django.urls.reverse(
                "company:group_detail",
                kwargs={"pk": self.group_a1.pk},
            ),
        )
        self.assertEqual(response.status_code, 200)

    def test_group_detail_access_forbidden_other_org(self):
        self.client.force_login(self.director)
        url = django.urls.reverse(
            "company:group_detail",
            kwargs={"pk": self.group_a2.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
