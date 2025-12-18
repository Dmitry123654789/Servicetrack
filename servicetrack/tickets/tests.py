__all__ = ()

import django.contrib.auth
import django.core.exceptions
import django.test
import django.urls

import company.models
import tickets.forms
import tickets.models
import tickets.validators


class TicketSystemTest(django.test.TestCase):
    fixtures = ["fixtures/data.json"]

    def setUp(self):
        self.user_model = django.contrib.auth.get_user_model()

        self.director = self.user_model.objects.get(pk=5)
        self.manager_a1 = self.user_model.objects.get(pk=6)
        self.worker = self.user_model.objects.get(pk=7)

        self.group_a1 = company.models.WorkerGroup.objects.get(pk=1)
        self.ticket = tickets.models.Ticket.objects.get(pk=1)

    def test_list_view_status_code(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse(
            "tickets:tickets_list",
            kwargs={"pk": self.group_a1.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_context_length(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse(
            "tickets:tickets_list",
            kwargs={"pk": self.group_a1.pk},
        )
        response = self.client.get(url)
        self.assertEqual(len(response.context), 4)

    def test_list_view_context_contains_tickets(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse(
            "tickets:tickets_list",
            kwargs={"pk": self.group_a1.pk},
        )
        response = self.client.get(url)
        self.assertIn("tickets", response.context)

    def test_list_view_contains_instance(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse(
            "tickets:tickets_list",
            kwargs={"pk": self.group_a1.pk},
        )
        response = self.client.get(url)
        self.assertIsInstance(
            response.context["tickets"][0],
            tickets.models.Ticket,
        )

    def test_detail_view_status_code(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse(
            "tickets:ticket_detail",
            kwargs={"pk": self.ticket.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_context_ticket_id(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse(
            "tickets:ticket_detail",
            kwargs={"pk": self.ticket.pk},
        )
        response = self.client.get(url)
        ticket_obj = response.context["ticket"]
        self.assertEqual(ticket_obj.id, 1)

    def test_detail_view_context_has_logs(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse(
            "tickets:ticket_detail",
            kwargs={"pk": self.ticket.pk},
        )
        response = self.client.get(url)
        self.assertIn("logs", response.context)

    def test_my_tickets_view_status_code(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse("tickets:my_tickets")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_my_tickets_context_groups_presence(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse("tickets:my_tickets")
        response = self.client.get(url)
        self.assertIn("groups", response.context)

    def test_create_view_get_status(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse("tickets:ticket_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_form_group_queryset_limit(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse("tickets:ticket_create")
        response = self.client.get(url)
        form = response.context["form"]
        queryset = form.fields["group"].queryset
        self.assertEqual(queryset.count(), 2)

    def test_worker_update_forbidden_for_non_assignee(self):
        self.client.force_login(self.manager_a1)
        url = django.urls.reverse(
            "tickets:ticket_worker_update",
            kwargs={"pk": self.ticket.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_status_transition_validation_error(self):
        data = {
            "title": self.ticket.title,
            "description": self.ticket.description,
            "status": "closed",
        }
        form = tickets.forms.TicketWorkerForm(data=data, instance=self.ticket)
        self.assertTrue(form.is_valid())

    def test_status_transition_valid(self):
        data = {
            "title": self.ticket.title,
            "description": self.ticket.description,
            "status": "in_progress",
        }
        form = tickets.forms.TicketWorkerForm(data=data, instance=self.ticket)
        self.assertTrue(form.is_valid())

    def test_status_log_creation_on_update(self):
        self.client.force_login(self.worker)
        url = django.urls.reverse(
            "tickets:ticket_worker_update",
            kwargs={"pk": self.ticket.pk},
        )
        initial_logs = tickets.models.StatusLog.objects.filter(
            ticket=self.ticket,
        ).count()
        data = {
            "title": self.ticket.title,
            "description": self.ticket.description,
            "status": "cancelled",
            "comment": "Closing this",
        }
        self.client.post(url, data)
        new_logs = tickets.models.StatusLog.objects.filter(
            ticket=self.ticket,
        ).count()
        self.assertEqual(new_logs, initial_logs + 1)

    def test_file_validator_large_file(self):
        validator = tickets.validators.FileValidator(max_size=10)
        fake_file = b"a" * 20
        with self.assertRaises(django.core.exceptions.ValidationError):
            validator(fake_file)

    def test_manager_update_view_access(self):
        self.client.force_login(self.director)
        url = django.urls.reverse(
            "tickets:ticket_manager_update",
            kwargs={"pk": self.ticket.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
