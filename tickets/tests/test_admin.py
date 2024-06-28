from django.test import TestCase
from django.contrib.auth.models import User
from tickets.models import AdminLog, Ticket
from django.urls import reverse

class AdminLogTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.login(username='admin', password='password')

    def test_create_ticket_log(self):
        self.client.post(reverse('create_ticket'), {
            'name': 'Test Ticket',
            'description': 'Test Description',
            'price': 100
        })
        log = AdminLog.objects.get(action='create', ticket_name='Test Ticket')
        self.assertEqual(log.admin.username, 'admin')
        self.assertEqual(log.action, 'create')
        self.assertEqual(log.ticket_name, 'Test Ticket')

    def test_delete_ticket_log(self):
        ticket = Ticket.objects.create(name='Test Ticket', description='Test Description', price=100)
        self.client.post(reverse('delete_ticket', args=[ticket.id]))
        log = AdminLog.objects.get(action='delete', ticket_name='Test Ticket')
        self.assertEqual(log.admin.username, 'admin')
        self.assertEqual(log.action, 'delete')
        self.assertEqual(log.ticket_name, 'Test Ticket')
