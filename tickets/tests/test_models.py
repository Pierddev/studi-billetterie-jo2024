from django.test import TestCase
from tickets.models import Ticket, AdminLog
from django.contrib.auth.models import User

class TicketModelTest(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(name='Test Ticket', description='Test Description', price=100)

    def test_ticket_creation(self):
        self.assertTrue(isinstance(self.ticket, Ticket))
        self.assertEqual(self.ticket.__str__(), self.ticket.name)

class AdminLogModelTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.ticket = Ticket.objects.create(name='Test Ticket', description='Test Description', price=100)
        self.log = AdminLog.objects.create(admin=self.admin_user, action='create', ticket_name=self.ticket.name)

    def test_admin_log_creation(self):
        self.assertTrue(isinstance(self.log, AdminLog))
        self.assertEqual(self.log.__str__(), f'{self.log.admin} {self.log.action} {self.log.ticket_name}')
