from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from tickets.models import Ticket, Cart, CartItem, Purchase, AdminLog
from unittest.mock import patch
import stripe

class TicketCreationTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.login(username='admin', password='password')

    def test_create_ticket(self):
        response = self.client.post(reverse('create_ticket'), {
            'name': 'Test Ticket',
            'description': 'Test Description',
            'price': 100
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ticket.objects.filter(name='Test Ticket').exists())
        self.assertTrue(AdminLog.objects.filter(action='create', ticket_name='Test Ticket').exists())

class TicketDeletionTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.login(username='admin', password='password')
        self.ticket = Ticket.objects.create(name='Test Ticket', description='Test Description', price=100)

    def test_delete_ticket(self):
        response = self.client.post(reverse('delete_ticket', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ticket.objects.filter(name='Test Ticket').exists())
        self.assertTrue(AdminLog.objects.filter(action='delete', ticket_name='Test Ticket').exists())